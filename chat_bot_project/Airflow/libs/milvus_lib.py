from log_lib import Log
from typing import List, Optional
from dataclasses import dataclass
from model_lib import Model
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from pydantic import BaseModel


class CollectionConfig:
    """Конфиг для БД"""

    NAME: str = "Документы"
    DIMENSION: int = 3072
    DESCRIPTION: str = "Эмбеддинги"
    CONSISTENCY_LEVEL: str = "Strong"
    AUTO_ID: bool = True

    @classmethod
    def get_fields(cls, dimension: int, text_len: int) -> List[FieldSchema]:
        """Поля для коллекции"""

        return [
            FieldSchema(
                name="id", dtype=DataType.INT64, is_primary=True, auto_id=cls.AUTO_ID
            ),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=text_len),
            FieldSchema(name="section", dtype=DataType.VARCHAR, max_length=200),
            FieldSchema(name="subsection", dtype=DataType.VARCHAR, max_length=200),
            FieldSchema(name="article", dtype=DataType.VARCHAR, max_length=10),
        ]


class IndexConfig:
    """Конфиг для индексов Malvus БД"""

    EMBEDDING_INDEX_NAME = "embedding_idx"
    INDEX_TYPE = "IVF_FLAT"
    METRIC_TYPE = "L2"
    INDEX_PARAMS = {"nlist": 128}


@dataclass
class DocumentData(BaseModel):
    """Дата класс документа"""

    text: str
    embedding: List[float]
    section: str
    subsection: str
    article: str


class MilvusDBClient:
    """Инициализация Милвус и операции с БД"""

    def __init__(self, LibLog: Log):
        self.logging: Log = LibLog
        self._connection_alias = "default"
        self.collection: Optional[Collection] = None
        self._is_connected = False

    def connect(self, host: str = "localhost", port: str = "19530") -> None:
        """Коннекшн"""
        try:
            connections.connect(alias=self._connection_alias, host=host, port=port)
            self._is_connected = True
            self.logging.log("Подключение к Milvus успешно!")
        except Exception as e:
            self.logging.error(f"Ошибка: {e}")
            raise

    def _validate_connection(self) -> None:
        """Проверка на коннекшн"""
        if not self._is_connected:
            raise ConnectionError("Нет коннекшена к Милвусу")

    def create_collection(self, name: str, dimension: int, text_len: int) -> None:
        """Создание коллекции"""
        self._validate_connection()

        self.dimension = dimension
        self.text_len = text_len

        if utility.has_collection(name):
            self.collection = Collection(name)
            self.logging.log(f"Коллекция уже существует: {name}")

        else:
            schema = CollectionSchema(
                fields=CollectionConfig.get_fields(self.dimension, self.text_len),
                description=CollectionConfig.DESCRIPTION,
            )

            self.collection = Collection(
                name=name,
                schema=schema,
                consistency_level=CollectionConfig.CONSISTENCY_LEVEL,
            )
            self.logging.log(f"Коллекция {name} успешно создана!")

    def create_index(self) -> None:
        """Cоздание индекса"""
        self._validate_connection()

        if not self.collection:
            raise ValueError("Коллекция не инициализирована")

        if self.collection.has_index():
            self.logging.log("Индекс уже существует")
        else:

            index_params = {
                "index_type": IndexConfig.INDEX_TYPE,
                "metric_type": IndexConfig.METRIC_TYPE,
                "params": IndexConfig.INDEX_PARAMS,
            }

            self.collection.create_index(
                field_name="embedding",
                index_params=index_params,
                index_name=IndexConfig.EMBEDDING_INDEX_NAME,
            )
            self.collection.load()
            self.logging.log("Индекс успешно создан")

    def insert_document(self, document: DocumentData) -> None:
        """
        Вставка дока в коллекцию
        """
        self._validate_connection()

        if not self.collection:
            raise ValueError("Коллекция не инициализирована")

        entities = [
            [document.embedding],
            [document.text],
            [document.section],
            [document.subsection],
            [document.article],
        ]

        try:
            self.collection.insert(entities)
            self.logging.log("Док успешно вставлен в коллекцию")
        except Exception as e:
            self.logging.error(f"Ошибка вставки: {e}")
            raise

    def search_answer(self, question: str, model_type: str = "notLocal", top_k=3):
        embedding = Model(model_type=model_type).get_embedding(question)

        if not embedding or len(embedding) != self.dimension:
            self.logging.warning(f"Некорректный эмбеддинг для вопроса: {question}")
            return []

        if not self.collection:
            raise ValueError("Коллекция не инициализирована")

        try:
            results = self.collection.search(
                data=[embedding],
                anns_field="embedding",
                param={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=top_k,
                output_fields=["text", "section", "article"],
            )

            return [
                {
                    "text": hit.entity.get("text"),
                    "section": hit.entity.get("section"),
                    "article": hit.entity.get("article"),
                    "distance": hit.distance,
                }
                for hit in results[0]
            ]

        except Exception as e:
            self.logging.warning(f"Ошибка поиска: {str(e)}")
            return []

    def close(self) -> None:
        """Закрыли коннекшн"""
        connections.disconnect(self._connection_alias)
        self._is_connected = False
        self.logging.log("Коннекш закрыт")
