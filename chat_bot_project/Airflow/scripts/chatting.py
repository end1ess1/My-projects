import os
import requests
import numpy as np
import re
import faiss
from dotenv import load_dotenv

def normalize(vector):
    return vector / np.linalg.norm(vector)

def get_embeddings(prompt, url: str):
    '''Получение эмбеддинга'''

    response = requests.post(url, json={"content": prompt})
    embedding = response.json()[0]['embedding']
    embedding_array = np.array(embedding)
    
    return normalize(embedding_array)

def get_embeddings(prompt, url: str):
    '''Получение эмбеддинга'''

    response = requests.post(url, json={"content": prompt})
    embedding = response.json()[0]['embedding']
    embedding_array = np.array(embedding)
    
    return embedding_array.astype('float32')


def split_document(document):
    '''Разделение документа на части по разметке #, ##, ###'''

    sections = re.split(r'(#+\s.*)', document)
    sections = [s.strip() for s in sections if s.strip()]
    result = []
    current_section = ""
    for section in sections:
        if section.startswith("#"):
            if current_section:
                result.append(current_section) 
            current_section = section
        else:
            current_section += "\n" + section
    if current_section:
        result.append(current_section)
    
    return result

def split_into_batches(text, batch_size: int = 1000):
    return [text[i:i + batch_size] for i in range(0, len(text), batch_size)]


def create_faiss_index(embeddings):
    '''Создание индекса FAISS и добавление эмбеддингов'''

    embeddings_array = np.vstack(embeddings).astype('float32') 

    d = embeddings_array.shape[1]

    index = faiss.IndexFlatL2(d)
    index.add(embeddings_array)
    return index

def search_faiss(query, index, documents, url):
    '''Поиск по запросу через FAISS и возвращение документа'''

    query_embedding = get_embeddings(query, url)
    _, I = index.search(query_embedding, k=1)
    return documents[I[0][0]]


def main():
    load_dotenv()
    
    document = ''

    for filename in os.listdir(os.getenv('TXT_DIR')):
        file_path = os.path.join(os.getenv('TXT_DIR'), filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            document += file.read() + "\n"

    # Шаг 1: Разделение документа на части
    #sections = split_document(document)
    sections = split_into_batches(document)
    
    # Шаг 2: Получение эмбеддингов для каждой части документа
    embeddings = [get_embeddings(section, os.getenv('URL')) for section in sections]
    
    # Шаг 3: Создание индекса FAISS
    index = create_faiss_index(embeddings)
    
    # Шаг 4: Пример поиска по запросу
    query = "Какие есть кафедры в МИИГАИК?"
    best_section = search_faiss(query, index, sections, os.getenv('URL'))
    
    print(f"Лучший ответ на запрос: \n{best_section}")


if __name__ == "__main__":
    main()


## ЗАГЛУШКА ###
def get_model_answer(text):
    return 'Привет! Меня зовут Гисик. Задавай любой вопрос!'











