import requests
import numpy as np

url = 'http://192.168.0.156:5000/embeddings'

def get_embeddings(prompt, url: str):
    '''Получение эмбеддинга'''

    response = requests.post(url, json={"content": prompt})
    embedding = response.json()[0]['embedding']

    return np.array(embedding)

answer = "Привет! Как у тебя дела?"
embeddings = get_embeddings(answer)

## Заглушка

def get_model_answer():
    return 'Привет! Меня зовут Гисик. Задавай любой вопрос!'
