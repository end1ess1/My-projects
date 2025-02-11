from pymilvus import connections, Collection, FieldSchema, DataType, CollectionSchema
import requests

# Конфигурация
MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'
EMBEDDING_URL = 'http://192.168.114.62:5001/embeddings'
COLLECTION_NAME = 'doc_embeddings'
DIMENSION = 3584

# Подключение к Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

# Создание коллекции (если не существует)
fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
    FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name='section', dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name='subsection', dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name='article', dtype=DataType.VARCHAR, max_length=50)
]

schema = CollectionSchema(fields, description='Document embeddings')
collection = Collection(COLLECTION_NAME, schema, consistency_level='Strong')

# Создание индекса (если не существует)
index_params = {
    'index_type': 'IVF_FLAT',
    'metric_type': 'L2',
    'params': {'nlist': 128}
}
collection.create_index(field_name='embedding', index_params=index_params)
collection.load()

# Получение эмбеддинга
def get_embedding(text: str) -> list:
    response = requests.post(EMBEDDING_URL, json={'content': text})
    return response.json()[0].get('embedding')[0]

# Вставка данных
def insert_data(data: dict):
    entities = [
        [get_embedding(data['text'])],
        [data['text']],
        [data['metadata']['section']],
        [data['metadata']['subsection'] or ''],
        [data['metadata']['article']]
    ]
    collection.insert(entities)
    print('Data inserted successfully')

# Пример использования
if __name__ == '__main__':
    sample_data = {
        "text": "Рэдклифф",
        "metadata": {
            "section": "III. Вступительные испытания",
            "subsection": None,
            "article": "38"
        }
    }
    #get_embedding(sample_data['text'])
    insert_data(sample_data)