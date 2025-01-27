import psycopg2
import os
from dotenv import load_dotenv
import redis
from typing import Tuple
import psycopg2.extensions
import redis.client


def connect_to_databases() -> Tuple[psycopg2.extensions.connection, redis.client.Redis]:

    load_dotenv()
    
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_DB = os.getenv("DATABASE_DB")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")

    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")
    REDIS_HOST = os.getenv("REDIS_HOST")

    postgres_connection = psycopg2.connect(dbname=DATABASE_DB,
                                            user=DATABASE_USER,
                                            password=DATABASE_PASSWORD,
                                            host=DATABASE_HOST,
                                            port=DATABASE_PORT)
    redis_connection = redis.StrictRedis(db=REDIS_DB,
                                        host=REDIS_HOST,
                                        port=REDIS_PORT)
    
    return postgres_connection, redis_connection