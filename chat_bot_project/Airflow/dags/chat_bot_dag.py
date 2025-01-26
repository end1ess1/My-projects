# Version 0.0.1

# Разработчик
# Документация
# Универ / Диплом / МИИГАИК / Тема

from airflow import DAG
from airflow.providers import PythonOperator

import os 
import sys
import yaml
import pathlib


file_path = pathlib.Path(__file__)
DAG_ID = '9999'
DAG_NAME = 'chat_bot_dag'
SCRIPTS_PATH = os.getenv("AIRFLOW_VAR_SCRIPTS", '/opt/airflow/scripts')

with open(os.path.join(SCRIPTS_PATH, f'{DAG_NAME}_params.yaml'), 'r') as ff:
    dag_config = yaml.full_load(ff)
    
application_args = [
    k 
    for pair in [
        ['--' + i, j]
        for i, j in dag_config['task_vars'].items()
        if j is not None
    ]
    for k in pair
]

apps = dag_config['dag_vars']['apps']
libs = dag_config['dag_vars']['libs']

with DAG(DAG_ID, **dag_config['dag_kwargs']) as dag:
    pass