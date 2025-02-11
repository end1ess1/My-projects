from pymilvus import connections, Collection
import requests
import numpy as np

# Конфигурация
MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'
EMBEDDING_URL = 'http://192.168.114.62:5001/embeddings'  # Исправленный URL
COLLECTION_NAME = 'doc_embeddings'

# Подключение к Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
collection.load()

def get_embedding(text: str) -> list:
    response = requests.post(EMBEDDING_URL, json={'content': text})
    return response.json()[0].get('embedding')[0]

def search_answer(question: str, top_k=3):
    # Получаем и проверяем эмбеддинг
    embedding = get_embedding(question)
    
    if not embedding or len(embedding) != 3584:  # Проверка размерности
        print("Некорректный эмбеддинг")
        return []

    try:
        # Выполняем поиск
        results = collection.search(
            data=[embedding],
            anns_field='embedding',
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=top_k,
            output_fields=['text', 'section', 'article']
        )
        
        return [{
            'text': hit.entity.get('text'),
            'section': hit.entity.get('section'),
            'article': hit.entity.get('article'),
            'distance': hit.distance
        } for hit in results[0]]
    
    except Exception as e:
        print(f"Ошибка поиска: {str(e)}")
        return []

# Пример использования
if __name__ == '__main__':
    
    # Проверка эмбеддинга для "Рэдклифф"
    embedding_redcliff = get_embedding("Рэдклифф")
    print(f"Размерность: {len(embedding_redcliff)}, Пример значений: {embedding_redcliff[:5]}")

    # Проверка эмбеддинга для целевого текста
    embedding_target = get_embedding("Перечень специальностей...")
    print(f"Размерность: {len(embedding_target)}, Пример значений: {embedding_target[:5]}")
    
    # question = "Перечень специальностей"
    # answers = search_answer(question)
    
    # for i, answer in enumerate(answers, 1):
    #     print(f"\nРезультат #{i}:")
    #     print(f"Текст: {answer['text']}")
    #     print(f"Раздел: {answer['section']}")
    #     print(f"Статья: {answer['article']}")
    #     print(f"Схожесть: {1 - answer['distance']:.2%}")  # Конвертация в проценты
