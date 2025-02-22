"""Полный пайплайн запуска Телеграм Бота

ВУЗ: Московский государственный университет геодезии и картографии (МИИГАИК)
Факультет: геоинформатики и информационной безопасности
Кафедра: информационно-измерительных систем
Группа: ИСиТ 4-1б
Разработчик: Абашин Егор Сергеевич

Очередность:
1. Первым запускается блок `Databases`, который включает в себя запуск и проверку доступности баз данных: PostgreSQL, Redis и Milvus.
2. Вторым запускается блок `Superset`, который отвечает за запуск и проверку доступности сервиса Superset.
3. Третьим запускается блок `LLM_model`, который запускает и проверяет доступность LLM.
4. Четвертым запускается блок `Telegram_bot`, который запускает и проверяет доступность Телеграм бота.

Краткое описание каждой таски:
- `send_start_message`: Отправляет сообщение в Телеграм о начале выполнения DAG.
- `send_end_message`: Отправляет сообщение в Телеграм об успешном завершении DAG.
- `send_databases_message`: Отправляет сообщение в Телеграм об успешном запуске всех баз данных.
- `send_success_postgre`: Отправляет сообщение в Телеграм об успешном запуске PostgreSQL.
- `send_success_redis`: Отправляет сообщение в Телеграм об успешном запуске Redis.
- `send_success_milvus`: Отправляет сообщение в Телеграм об успешном запуске Milvus.
- `send_superset_message`: Отправляет сообщение в Телеграм об успешном запуске Superset.
- `send_llm_message`: Отправляет сообщение в Телеграм об успешном запуске LLM.
- `send_telegramBot_message`: Отправляет сообщение в Телеграм об успешном запуске Телеграм бота.
- `Preprocessing`, `Get_Embeddings`, `Load_to_Milvus`: Таски, отвечающие за предобработку, получение эмбеддингов и загрузку документов в Milvus.

Краткое описание сервисов:
- **PostgreSQL**: Реляционная база данных, используемая для хранения структурированных данных.
- **Redis**: In-memory база данных, используемая для кэширования и хранения временных данных.
- **Milvus**: Векторная база данных, используемая для хранения и поиска векторных представлений документов.
- **Superset**: Инструмент для визуализации данных и создания дашбордов.
- **LLM_model**: LLM модель, на основе которой потвечает Telegram бот.
- **Telegram_bot**: Бот, который взаимодействует с пользователями через Telegram.

Дополнительная информация:
- Для корректной работы DAG необходимо наличие всех переменных окружения, указанных в `.env` файле.
- Время выполнения DAG зависит от скорости запуска и проверки всех сервисов, а также от объема данных, загружаемых в Milvus.
- В случае ошибок в процессе выполнения DAG, в Телеграм будет отправлено соответствующее уведомление.
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

DAG_NAME = "start_telegram_chat_bot_dag"

CHAT_ID = os.getenv("CHAT_ID")
TOKEN = os.getenv("AIRFLOW_BOT_API")

CONFIG_PATH = os.getenv("CONFIG_PATH")

SUPERSET_BASH_COMMAND = os.getenv("SUPERSET_BASH_COMMAND")
LLM_BASH_COMMAND = os.getenv("LLM_BASH_COMMAND")
TELEGRAM_BASH_COMMAND = os.getenv("TELEGRAM_BASH_COMMAND")
POSTGRESQL_BASH_COMMAND = os.getenv("POSTGRESQL_BASH_COMMAND")
REDIS_BASH_COMMAND = os.getenv("REDIS_BASH_COMMAND")
MILVUS_BASH_COMMAND = os.getenv("MILVUS_BASH_COMMAND")
LOAD_DOCS_BASH_COMMAND = os.getenv("LOAD_DOCS_BASH_COMMAND")

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


with DAG(DAG_NAME, doc_md=__doc__, **dag_config["dag_kwargs"]) as dag:
    start_message = PythonOperator(
        task_id="send_start_message",
        python_callable=send_telegram_message,
        op_kwargs={"message": "Даг успешно запустился!"},
    )

    end_message = PythonOperator(
        task_id="send_end_message",
        python_callable=send_telegram_message,
        op_kwargs={
            "message": "Даг успешно завершил работу! Пайплайн польностью выполнен"
        },
    )

    with TaskGroup("Services", dag=dag) as services:
        with TaskGroup("Databases", dag=dag) as databases:
            db_message = PythonOperator(
                task_id="send_databases_message",
                python_callable=send_telegram_message,
                op_kwargs={"message": "Базы данных успешно запустились!"},
            )

            with TaskGroup("Postgre_Database", dag=dag) as postgresql:
                posgtre_message = PythonOperator(
                    task_id="send_success_postgre",
                    python_callable=send_telegram_message,
                    op_kwargs={"message": "БД Posgtre успешно запустилась!"},
                )

                postgres_sensor = BashSensor(
                    task_id="postgres_sensor",
                    bash_command=POSTGRESQL_BASH_COMMAND_SENSOR,
                    timeout=600,
                    poke_interval=10,
                    mode="poke",
                )

                start_postgre = BashOperator(
                    task_id="PosgtreSQL", bash_command=POSTGRESQL_BASH_COMMAND
                )

                start_postgre >> postgres_sensor >> posgtre_message

            with TaskGroup("Redis_Database", dag=dag) as redis:
                redis_message = PythonOperator(
                    task_id="send_success_redis",
                    python_callable=send_telegram_message,
                    op_kwargs={"message": "БД Redis успешно запустилась!"},
                )

                redis_sensor = BashSensor(
                    task_id="redis_sensor",
                    bash_command=REDIS_BASH_COMMAND_SENSOR,
                    timeout=600,
                    poke_interval=10,
                    mode="poke",
                )

                start_redis = BashOperator(
                    task_id="Redis", bash_command=REDIS_BASH_COMMAND
                )

                start_redis >> redis_sensor >> redis_message

            with TaskGroup("Milvus_Database", dag=dag) as milvus:
                milvus_message = PythonOperator(
                    task_id="send_success_milvus",
                    python_callable=send_telegram_message,
                    op_kwargs={"message": "БД Milvus успешно запустилась!"},
                )

                milvus_sensor = BashSensor(
                    task_id="milvus_sensor",
                    bash_command=MILVUS_BASH_COMMAND_SENSOR,
                    timeout=600,
                    poke_interval=10,
                    mode="poke",
                )

                start_milvus = BashOperator(
                    task_id="Milvus", bash_command=MILVUS_BASH_COMMAND
                )

                with TaskGroup("Documents", dag=dag) as documents:
                    success_downloading_message = PythonOperator(
                        task_id="send_success_downloading_message",
                        python_callable=send_telegram_message,
                        op_kwargs={
                            "message": "Документы успешно загружены в БД Milvus."
                        },
                    )

                    preprocessing_docs = DummyOperator(task_id="Preprocessing")
                    load_docs_to_db = BashOperator(
                        task_id="Load_docs_to_Milvus",
                        bash_command=LOAD_DOCS_BASH_COMMAND,
                    )

                    preprocessing_docs >> load_docs_to_db >> success_downloading_message

                start_milvus >> milvus_sensor >> milvus_message >> documents

            postgresql >> db_message
            redis >> db_message
            milvus >> db_message

        with TaskGroup("Superset", dag=dag) as superset:
            superset_message = PythonOperator(
                task_id="send_superset_message",
                python_callable=send_telegram_message,
                op_kwargs={"message": "Суперсет успешно запустился!"},
            )

            superset_sensor = BashSensor(
                task_id="superset_sensor",
                bash_command=SUPERSET_BASH_COMMAND_SENSOR,
                timeout=600,
                poke_interval=10,
                mode="poke",
            )

            start_superset = BashOperator(
                task_id="Superset", bash_command=SUPERSET_BASH_COMMAND
            )

            start_superset >> superset_sensor >> superset_message

        with TaskGroup("LLM_model", dag=dag) as llm:
            llm_message = PythonOperator(
                task_id="send_llm_message",
                python_callable=send_telegram_message,
                op_kwargs={"message": "Модель успешно запустилась!"},
            )

            llm_sensor = BashSensor(
                task_id="llm_sensor",
                bash_command=LLM_BASH_COMMAND_SENSOR,
                timeout=600,
                poke_interval=10,
                mode="poke",
            )

            start_model = BashOperator(task_id="Model", bash_command=LLM_BASH_COMMAND)

            start_model >> llm_sensor >> llm_message

        with TaskGroup("Telegram_bot", dag=dag) as tg_bot:
            tg_message = PythonOperator(
                task_id="send_telegramBot_message",
                python_callable=send_telegram_message,
                op_kwargs={"message": "Телеграм бот успешно запустился!"},
            )

            tg_sensor = BashSensor(
                task_id="telegram_bot_sensor",
                bash_command=TELEGRAM_BASH_COMMAND_SENSOR,
                timeout=600,
                poke_interval=10,
                mode="poke",
            )

            start_telegram_bot = BashOperator(
                task_id="TelegramBot", bash_command=TELEGRAM_BASH_COMMAND
            )

            start_telegram_bot >> tg_sensor >> tg_message

        databases >> superset >> llm
        databases >> superset >> tg_bot

    start_message >> services >> end_message
