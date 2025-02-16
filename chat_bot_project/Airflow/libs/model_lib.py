from dataclasses import dataclass, fields
import argparse
import requests
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

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


class Model(metaclass=MetaClass):
    local_url: str = os.getenv('LOCAL_URL')
    api_key: str = os.getenv('API_KEY')
    base_url: str = os.getenv('BASE_URL')
    model_type: str = 'API'
    
    def _normalize_embedding(self, embedding):
        norm_embedding = embedding / np.linalg.norm(embedding)
        return norm_embedding
    
    def get_embedding(self, text: str) -> list:
        if self.model_type != 'API':
            response = requests.post(self.local_url, json={'content': text})
            embedding = response.json()[0].get('embedding')[0]
            norm_embedding = self._normalize_embedding(embedding)

            return norm_embedding

        else:
            client = OpenAI(api_key=self.api_key,
                            base_url=self.base_url)
            
            embedding = client.embeddings.create(
                        model="text-embedding-3-large",
                        input=text,
                        encoding_format="float"
                        )
            
            norm_embedding = self._normalize_embedding(embedding)
            
            return embedding
