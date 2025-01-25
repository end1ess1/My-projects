#import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import requests

def encode(text, server_url="http://192.168.0.156:5000/embedding"):
    """
    Отправляет текст на сервер для получения векторного представления.
    
    Args:
        text (str): Текст для преобразования в вектор.
        server_url (str): URL сервера с вашей моделью.
        
    Returns:
        np.ndarray: Векторное представление текста.
    """
    data = {"text": text}
    response = requests.post(server_url, json=data)
    
    if response.status_code == 200:
        embedding = response.json().get("embedding")
        if embedding:
            return np.array(embedding)  # Преобразуем вектор в массив numpy
        else:
            raise ValueError("Сервер вернул пустой вектор")
    else:
        raise ConnectionError(f"Ошибка: {response.status_code}, {response.text}")

# Допустим, у вас есть функция для преобразования текста в векторы
def text_to_vector(text, model):
    # Эта функция должна преобразовывать текст в вектор с помощью вашей модели
    return model.encode(text)  # Предположим, что у вас есть метод `encode` для модели

# Функция для загрузки текста из файла
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Пример работы с вашим текстом и локальной моделью
def retrieve_local_model(query, model):
    # Загрузка текста
    text = load_text('data.txt')

    # Разбиение текста на предложения или абзацы
    paragraphs = text.split("\n")

    # Преобразуем все абзацы в векторы
    vectors = [text_to_vector(paragraph, model) for paragraph in paragraphs]

    # Преобразуем запрос в вектор
    query_vector = text_to_vector(query, model)

    # Вычисление косинусного сходства для поиска наиболее похожего текста
    similarities = cosine_similarity([query_vector], vectors)
    most_similar_idx = np.argmax(similarities)

    # Получаем наиболее похожий абзац
    answer = paragraphs[most_similar_idx]
    
    # Выводим ответ
    print("Ответ:", answer)

    return answer

# Пример вызова функции
# Пожалуйста, замените `your_model` на вашу локальную модель
# например, это может быть `sentence-transformers` модель или любая другая
query = "Расскажи о чем-то из документа"
# model = YourLocalModel()  # Инициализация вашей модели
# retrieve_local_model(query, model)