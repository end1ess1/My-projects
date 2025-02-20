"""Полный пайплайн запуска Телеграм Бота

Очередность:
Первым запускается ...
Вторым ...

Кратко описание каждой таски
Краткое описание сервисов



"""

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.telegram.hooks.telegram import TelegramHook
from airflow.sensors.base import BaseSensorOperator
import yaml
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

DAG_NAME = "chat_bot_dag"

CHAT_ID = os.getenv("CHAT_ID")
TOKEN = os.getenv("AIRFLOW_BOT_API")

CONFIG_PATH = os.getenv("CONFIG_PATH")

SUPERSET_BASH_COMMAND = os.getenv("SUPERSET_BASH_COMMAND")
LLM_BASH_COMMAND = os.getenv("LLM_BASH_COMMAND")
TELEGRAM_BASH_COMMAND = os.getenv("TELEGRAM_BASH_COMMAND")
POSTGRESQL_BASH_COMMAND = os.getenv("POSTGRESQL_BASH_COMMAND")
REDIS_BASH_COMMAND = os.getenv("REDIS_BASH_COMMAND")
MILVUS_BASH_COMMAND = os.getenv("MILVUS_BASH_COMMAND")

SUPERSET_BASH_COMMAND_SENSOR = os.getenv("SUPERSET_BASH_COMMAND_SENSOR")
LLM_BASH_COMMAND_SENSOR = os.getenv("LLM_BASH_COMMAND_SENSOR")
TELEGRAM_BASH_COMMAND_SENSOR = os.getenv("TELEGRAM_BASH_COMMAND_SENSOR")
POSTGRESQL_BASH_COMMAND_SENSOR = os.getenv("POSTGRESQL_BASH_COMMAND_SENSOR")
REDIS_BASH_COMMAND_SENSOR = os.getenv("REDIS_BASH_COMMAND_SENSOR")
MILVUS_BASH_COMMAND_SENSOR = os.getenv("MILVUS_BASH_COMMAND_SENSOR")


def send_telegram_message(message):
    hook = TelegramHook(
        telegram_conn_id="telegram_default", token=TOKEN, chat_id=CHAT_ID
    )
    hook.send_message({"text": message})


class BashSensor(BaseSensorOperator):
    def __init__(self, bash_command, *args, **kwargs):
        super(BashSensor, self).__init__(*args, **kwargs)
        self.bash_command = bash_command

    def poke(self, context):
        try:
            subprocess.check_call(self.bash_command, shell=True)
            return True
        except subprocess.CalledProcessError:
            return False


with open(os.path.join(CONFIG_PATH, f"{DAG_NAME}_params.yaml"), "r") as ff:
    dag_config = yaml.full_load(ff)


with DAG(DAG_NAME, **dag_config["dag_kwargs"]) as dag:
    start_message = PythonOperator(
        task_id="send_start_message",
        python_callable=send_telegram_message,
        op_kwargs={"message": "Даг успешно запустился!"},
    )

    with TaskGroup("Services", dag=dag) as services:
        superset_message = PythonOperator(
            task_id="send_superset_message",
            python_callable=send_telegram_message,
            op_kwargs={"message": "Суперсет успешно запустился!"},
        )

        telegram_llm_message = PythonOperator(
            task_id="send_llm_telegram_message",
            python_callable=send_telegram_message,
            op_kwargs={"message": "Модель и тг бот успешно запустились!"},
        )

        superset_sensor = BashSensor(
            task_id="superset_sensor",
            bash_command=SUPERSET_BASH_COMMAND_SENSOR,
            timeout=600,
            poke_interval=10,
            mode="poke",
        )

        llm_sensor = BashSensor(
            task_id="llm_sensor",
            bash_command=LLM_BASH_COMMAND_SENSOR,
            timeout=600,
            poke_interval=10,
            mode="poke",
        )

        telegram_bot_sensor = BashSensor(
            task_id="telegram_bot_sensor",
            bash_command=TELEGRAM_BASH_COMMAND_SENSOR,
            timeout=600,
            poke_interval=10,
            mode="poke",
        )

        start_superset = BashOperator(
            task_id="Superset", bash_command=SUPERSET_BASH_COMMAND
        )

        start_model = BashOperator(task_id="Model", bash_command=LLM_BASH_COMMAND)

        start_telegram_bot = BashOperator(
            task_id="TelegramBot", bash_command=TELEGRAM_BASH_COMMAND
        )

        with TaskGroup("Databases", dag=dag) as databases:
            db_message = PythonOperator(
                task_id="send_databases_message",
                python_callable=send_telegram_message,
                op_kwargs={"message": "Базы данных успешно запустились!"},
            )

            postgres_sensor = BashSensor(
                task_id="postgres_sensor",
                bash_command=POSTGRESQL_BASH_COMMAND_SENSOR,
                timeout=600,
                poke_interval=10,
                mode="poke",
            )

            redis_sensor = BashSensor(
                task_id="redis_sensor",
                bash_command=REDIS_BASH_COMMAND_SENSOR,
                timeout=600,
                poke_interval=10,
                mode="poke",
            )

            milvus_sensor = BashSensor(
                task_id="milvus_sensor",
                bash_command=MILVUS_BASH_COMMAND_SENSOR,
                timeout=600,
                poke_interval=10,
                mode="poke",
            )

            start_postgre = BashOperator(
                task_id="PosgtreSQL", bash_command=POSTGRESQL_BASH_COMMAND
            )

            start_redis = BashOperator(task_id="Redis", bash_command=REDIS_BASH_COMMAND)

            start_milvus = BashOperator(
                task_id="Milvus", bash_command=MILVUS_BASH_COMMAND
            )

            start_postgre >> postgres_sensor >> db_message
            start_redis >> redis_sensor >> db_message
            start_milvus >> milvus_sensor >> db_message

        (
            databases
            >> start_superset
            >> superset_sensor
            >> superset_message
            >> start_model
            >> llm_sensor
            >> telegram_llm_message
        )
        (
            databases
            >> start_superset
            >> superset_sensor
            >> superset_message
            >> start_telegram_bot
            >> telegram_bot_sensor
            >> telegram_llm_message
        )

    DummyOperator()

    with TaskGroup("Services", dag=dag) as documents:
        pass

    start_message >> services >> documents
