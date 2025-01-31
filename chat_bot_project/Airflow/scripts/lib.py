from dataclasses import dataclass, fields
import argparse
from typing import List, Union, Optional
import psycopg2.extensions
from datetime import datetime
import redis.client


class MetaClass(type):
    def __new__(cls, name, bases, dct):
        old = super().__new__(cls, name, bases, dct)
        return dataclass(old)

class ModelArgs(metaclass=MetaClass):

    __description__ = {
        'llama_server_path': 'Путь до сервера',
        'model_path': 'Путь до модели',
        'ngl': 'Number of GPU Layers - кол-во слоев',
        'context_size': 'Контекстное окно, которое модель учитывает  при генерации ответа',
        'host': 'Порт',
        'port': 'Хост',
    }

    __mapping__ = {
        int: int,
        str: str,
        dict: str,
        list: str,
        bool: bool
    }

    llama_server_path: str
    model_path: str
    ngl: str
    context_size: str
    host: str
    port: str

    @classmethod
    def parse_base_args(cls):
        parser = argparse.ArgumentParser('Параметры для модели')
        for field in fields(cls):
            parser.add_argument(f'--{field.name}', type=field.type, help=cls.__description__[field.name])
        return parser.parse_args()


class Log(metaclass=MetaClass):
    postgresql_conn: psycopg2.extensions.connection
    redis_conn: redis.client.Redis
    script_name : str
    log_table_name: str='scripts_logs'
    
    def __post_init__(self) -> None:
        self._setup_table()

    def _setup_table(self) -> None:

        __comments__  = {
            'id': 'Уникальный идентификатор записи',
            'script_name': 'Имя, обязательно для заполнения',
            'processed_dttm': 'Дата и время, обязательно для заполнения',
            'level': 'Уровень логирования (например: log, error, warning)',
            'comment': 'Комментарий (может быть NULL)'
        }

        with self.postgresql_conn.cursor() as cur:
            cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS {self.log_table_name} (
                            id SERIAL PRIMARY KEY,
                            script_name VARCHAR(50) NOT NULL,
                            processed_dttm VARCHAR(50) NOT NULL,
                            level VARCHAR(10) NOT NULL,
                            comment TEXT
                        );
                        """)
            
            for col in __comments__:
                cur.execute(f"COMMENT ON COLUMN {self.log_table_name}.{col} IS '{__comments__[col]}'")
            
            cur.execute(f"COMMENT ON TABLE {self.log_table_name} IS 'Таблица для логирования скриптов'")
            
            self.postgresql_conn.commit()


    def _redis_caching_expire(self, comment: str, level: str):
        __logs_entry__ = {
            'processed_dttm': str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')),
            'level': level,
            'comment': comment
        }

        self.redis_conn.hset(name=self.script_name, mapping=__logs_entry__)
        self.redis_conn.expire(name=self.script_name, time=86400)
    
    
    def insert(self, comment: str, level: str) -> None:
        with self.postgresql_conn.cursor() as cur:
            cur.execute(f"""
                        INSERT INTO {self.log_table_name} (
                            script_name,
                            processed_dttm,
                            level,
                            comment
                            )
                        VALUES (
                            '{self.script_name}',
                            '{str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))}',
                            '{level}',
                            '{comment}'
                        );"""
                        )
        
            self.postgresql_conn.commit()
        
        self._redis_caching_expire(comment=comment, level=level)
    
    
    def error(self, comment: str, level: str='error')  -> None:
        
        self.insert(comment, level)
        
    
    def warning(self, comment: str, level: str='warning')  -> None:
        
        self.insert(comment, level)
        
    
    def log(self, comment: str, level: str='log')  -> None:
        
        self.insert(comment, level)
        
    
    def success(self, comment: str, level: str='success')  -> None:
        
        self.insert(comment, level)
        
    def finish(self, comment: str='Завершение работы', level: str='finish')  -> None:
        
        self.insert(comment, level)
        self.postgresql_conn.close()
        self.redis_conn.close()
    
    ###

    def insert_llm_log(self, user_id: str, first_name: str, last_name: str, username: str, chat_id: str,
                       question: str, answer: str, question_date: datetime, answer_date: datetime,
                       language_code: str, model_version: str, log_table_name: str) -> str:
        with self.postgresql_conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {log_table_name} (
                    user_id,
                    first_name,
                    last_name,
                    username,
                    chat_id,
                    question,
                    answer,
                    question_length,
                    answer_length,
                    response_time_s,
                    language_code,
                    question_date,
                    answer_date,
                    model_version
                )
                VALUES (
                    '{user_id}',
                    '{str(first_name)}',
                    '{str(last_name)}',
                    '{str(username)}',
                    '{chat_id}',
                    '{str(question)}',
                    '{str(answer)}',
                    '{str(len(question))}',
                    '{str(len(answer))}',
                    '{(answer_date-question_date).total_seconds()}',
                    '{str(language_code)}',
                    '{question_date}',
                    '{answer_date}',
                    '{str(model_version)}'
                );
            """)
            
            self.postgresql_conn.commit()

        __logs_entry__ = {
            'user_id': str(user_id),
            'first_name': str(first_name),
            'last_name': str(last_name),
            'username': str(username),
            'chat_id': str(chat_id),
            'question': str(question),
            'answer': str(answer),
            'question_length': str(len(question)),
            'answer_length': str(len(answer)),
            'response_time_s': str((answer_date-question_date).total_seconds()),
            'language_code': str(language_code),
            'question_date': str(question_date),
            'answer_date': str(answer_date)
        }

        self.redis_conn.hset(name=model_version, mapping=__logs_entry__)
        self.redis_conn.expire(name=model_version, time=86400)


class LogRetriever(metaclass=MetaClass):
    postgresql_conn: psycopg2.extensions.connection
    redis_conn: redis.client.Redis
    
    def get_logs(self, key: str):
        logs = self.redis_conn.hgetall(key)
        
        if logs:
            return {k.decode(): v.decode() for k, v in logs.items()}
        else:
            with self.postgresql_conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {Log.log_table_name} WHERE key = {key}")
                logs = cur.fetchall()
            return logs or "Логи не найдены."



        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    