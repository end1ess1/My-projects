"""Полный пайплайн запуска Телеграм Бота

Очередность:
Первым запускается ...
Вторым ...

Кратко описание каждой таски
Краткое описание сервисов



"""


from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.telegram.hooks.telegram import TelegramHook
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = os.getenv('CHAT_ID')
TOKEN = os.getenv('AIRFLOW_BOT_API')

# Функция для отправки сообщения
def send_telegram_message():
    hook = TelegramHook(telegram_conn_id='telegram_default', token=TOKEN, chat_id=CHAT_ID)
    hook.send_message( {
        'text': 'смска от Airflow'
    })


with open(os.path.join('/mnt/c/Users/My End_1ess C/Documents/Диплом/MyGithub/end1ess1/chat_bot_project/Airflow/Config',
                       f'chat_bot_dag_params.yaml'), 'r') as ff:
    dag_config = yaml.full_load(ff)


with DAG('TEST_TG_INFO', **dag_config['dag_kwargs']) as dag:
    start_message = PythonOperator(
        task_id='START_MESSAGE',
        python_callable=send_telegram_message,
    )
