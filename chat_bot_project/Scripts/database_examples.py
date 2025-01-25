import psycopg2
from lib import Log
from time import sleep
import redis
from rich.traceback import install
install(show_locals=True)

postgre_db_params = {
    'dbname': 'preprod_db',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': '5433'
}

redis_db_params = {
    'db': '0',
    'host': 'localhost',
    'port': '6379'
}


r = redis.StrictRedis(**redis_db_params)
conn = psycopg2.connect(**postgre_db_params)

logging = Log(posgtresql_conn=conn, redis_conn=r, script_name='test_postgre_sql.py')
logging.error('Ошибка')
sleep(1)
logging.warning('Предупреждение')
sleep(1)
logging.log('Обычный лог')
sleep(1)
logging.success('Успех')