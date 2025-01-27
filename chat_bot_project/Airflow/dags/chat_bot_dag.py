from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
import yaml
import sys
import os

#AG_ID = '1642_77_'
DAG_NAME = 'chat_bot_dag'
SCRIPTS_PATH = os.getenv("AIRFLOW_VAR_SCRIPTS", '/opt/airflow/scripts')
CONFIG_PATH = os.getenv("AIRFLOW_VAR_CONFIG", '/opt/airflow/config')

sys.path.append(SCRIPTS_PATH)
sys.path.append(CONFIG_PATH)

from testik import create_file

with open(os.path.join(CONFIG_PATH, f'{DAG_NAME}_params.yaml'), 'r') as ff:
    dag_config = yaml.full_load(ff)

# Определение DAG
with DAG(DAG_NAME, **dag_config['dag_kwargs']) as dag:
    # Оператор Dummy
    start = DummyOperator(
        task_id='start'
    )

    # Оператор Python
    execute_script = PythonOperator(
        task_id='run_python_script',
        python_callable=create_file  # Передаем функцию
    )

    # Еще один Dummy
    end = DummyOperator(
        task_id='end'
    )

    # Установка последовательности выполнения
    start >> execute_script >> end