from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import time

connections.connect(host="localhost", port="19530")

collection_name = "demo_collection"
dimension = 3
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension)
]
schema = CollectionSchema(fields=fields, description="Тестовая коллекция")
collection = Collection(name=collection_name, schema=schema)
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128}
}


if utility.has_collection(collection_name):
    print(f"Дроп сущ коллекции: {collection_name}")
    utility.drop_collection(collection_name)
    time.sleep(1)


collection.create_index(field_name="embedding", index_params=index_params)

collection.load()

data = [
    [0.1, 0.2, 0.3],
]

try:
    insert_result = collection.insert({"embedding": data[0]})
    print(f"Успешно")
    collection.flush()
except Exception as e:
    print(f"Ошибк: {str(e)}")
    raise