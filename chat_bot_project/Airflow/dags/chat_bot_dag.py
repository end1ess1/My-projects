"""Полный пайплайн запуска Телеграм Бота

Очередность:
Первым запускается ...
Вторым ...

Кратко описание каждой таски
Краткое описание сервисов



"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.telegram.hooks.telegram import TelegramHook
import yaml
import os
from dotenv import load_dotenv

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


# Функция для отправки сообщения
def send_telegram_message():
    hook = TelegramHook(
        telegram_conn_id="telegram_default", token=TOKEN, chat_id=CHAT_ID
    )
    hook.send_message({"text": ("Даг успешно запустился!")})


with open(os.path.join(CONFIG_PATH, f"{DAG_NAME}_params.yaml"), "r") as ff:
    dag_config = yaml.full_load(ff)


with DAG(DAG_NAME, **dag_config["dag_kwargs"]) as dag:
    start_message = PythonOperator(
        task_id="START_MESSAGE", python_callable=send_telegram_message
    )

    with TaskGroup("Services", dag=dag) as services:
        start_superset = BashOperator(
            task_id="Superset", bash_command=SUPERSET_BASH_COMMAND
        )

        start_model = BashOperator(task_id="Model", bash_command=LLM_BASH_COMMAND)

        start_telegram_bot = BashOperator(
            task_id="TelegramBot", bash_command=TELEGRAM_BASH_COMMAND
        )

        with TaskGroup("Databases", dag=dag) as databases:
            start_postgre = BashOperator(
                task_id="PosgtreSQL", bash_command=POSTGRESQL_BASH_COMMAND
            )

            start_redis = BashOperator(task_id="Redis", bash_command=REDIS_BASH_COMMAND)

            start_milvus = BashOperator(
                task_id="Milvus", bash_command=MILVUS_BASH_COMMAND
            )

        databases >> start_superset >> start_model
        databases >> start_superset >> start_telegram_bot

    start_message >> services
