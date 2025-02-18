from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.docker.operators.docker import DockerOperator
import yaml
import sys
import os

DAG_NAME = 'chat_bot_dag'
SCRIPTS_PATH = os.getenv("AIRFLOW_VAR_SCRIPTS", '/opt/airflow/scripts')
CONFIG_PATH = os.getenv("AIRFLOW_VAR_CONFIG", '/opt/airflow/config')
DATABASES_PATH = os.getenv("AIRFLOW_VAR_DATABASES", '/opt/airflow/databases')

sys.path.append(SCRIPTS_PATH)
sys.path.append(CONFIG_PATH)
sys.path.append(DATABASES_PATH)

with open(os.path.join(CONFIG_PATH, f'{DAG_NAME}_params.yaml'), 'r') as ff:
    dag_config = yaml.full_load(ff)

with DAG(DAG_NAME, **dag_config['dag_kwargs']) as dag:
    start = DummyOperator(
        task_id='Start'
    )
    with TaskGroup("Services", dag=dag) as services:
        start_superset = DummyOperator(
        task_id="Superset"
        )
        
        start_milvus = DockerOperator(
            task_id="run_milvus",
            image="docker:latest",
            command="docker-compose -f /opt/airflow/databases/Milvus/docker-compose.yml up -d",
            docker_url="unix://var/run/docker.sock",  # Указываем URL сокета Docker
            network_mode="host",  # Если нужно использовать хостовую сеть
            dag=dag,
        )
        
        start_model = DummyOperator(
            task_id="Model",
        )
        
        start_telegram_bot = DummyOperator(
            task_id="TelegramBot",
        )
        
        start_superset >> start_model >> start_telegram_bot
        start_milvus >> start_model >> start_telegram_bot
    
    end = DummyOperator(
        task_id='End'
    )
        
    start >> services >> end