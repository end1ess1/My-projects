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

DAG_NAME = 'chat_bot_dag'
CHAT_ID = os.getenv('CHAT_ID')
TOKEN = os.getenv('AIRFLOW_BOT_API')

# Функция для отправки сообщения
def send_telegram_message(text):
    hook = TelegramHook(telegram_conn_id='telegram_default', token=TOKEN, chat_id=CHAT_ID)
    hook.send_message( {
        'text': text
    })


with open(os.path.join('/mnt/c/Users/My End_1ess C/Documents/Диплом/MyGithub/end1ess1/chat_bot_project/Airflow/Config',
                       f'{DAG_NAME}_params.yaml'), 'r') as ff:
    dag_config = yaml.full_load(ff)


with DAG(DAG_NAME, **dag_config['dag_kwargs']) as dag:
    start_message = PythonOperator(
        task_id='START_MESSAGE',
        python_callable=send_telegram_message('Даг успешно запустился!'),
    )

    with TaskGroup("Services", dag=dag) as services:
        start_superset = DummyOperator(
        task_id="Superset"
        )

        start_model = DummyOperator(
            task_id="Model",
        )

        start_telegram_bot = DummyOperator(
            task_id="TelegramBot",
        )

        with TaskGroup("Databases", dag=dag) as databases:
        
            start_postgre = BashOperator(
                task_id='PosgtreSQL',
                bash_command='sudo docker-compose -f "/mnt/c/Users/My End_1ess C/Documents/Диплом/MyGithub/end1ess1/chat_bot_project/Databases/PostgreSQL/docker-compose.yml" up -d',
                )

            start_redis = BashOperator(
                task_id='Redis',
                bash_command='sudo docker-compose -f "/mnt/c/Users/My End_1ess C/Documents/Диплом/MyGithub/end1ess1/chat_bot_project/Databases/Redis/docker-compose.yml" up -d',
                )

            start_milvus = BashOperator(
                task_id='Milvus',
                bash_command='sudo docker-compose -f "/mnt/c/Users/My End_1ess C/Documents/Диплом/MyGithub/end1ess1/chat_bot_project/Databases/Milvus/docker-compose.yml" up -d',
                )

        databases >> start_superset >> start_telegram_bot
        databases >> start_model >>  start_telegram_bot

    end_message = PythonOperator(
        task_id='FINISH_MESSAGE',
        python_callable=send_telegram_message('Даг успешно отработал!'),
    )
