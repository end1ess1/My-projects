import requests
import numpy as np
import re
import faiss


url = 'http://192.168.0.156:5000/embeddings'


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
    document = """
    ### Кафедры МИИГАиК

#### Геодезический факультет (ГФ)
- Кафедра геодезии
- Кафедра прикладной геодезии
- Кафедра высшей геодезии
- Кафедра астрономии и космической геодезии
- Кафедра фотограмметрии
- Кафедра аэрокосмических съемок

#### Картографический факультет
- Кафедра картографии
- Кафедра визуализации геоданных и картографического дизайна
- Кафедра географии
- Кафедра космического мониторинга и экологии
- Кафедра цифровой картографии

#### Факультет оптического приборостроения
- Кафедра оптико-электронных приборов
- Кафедра прикладной оптики
- Кафедра проектирования оптических приборов
- Кафедра технологии оптического приборостроения
- Лаборатория когерентной оптики

#### Факультет геоинформатики и информационной безопасности
- Кафедра информационно-измерительных систем
- Кафедра прикладной информатики
- Кафедра геоинформационных систем и технологий

#### Факультет управления территориями
- Кафедра земельного права и государственной регистрации недвижимости
- Кафедра управления недвижимостью и развитием территорий
- Кафедра землеустройства и кадастров
- Кафедра экономики
- Кафедра уголовного права и процесса
- Кафедра гражданского права и процесса

#### Факультет архитектуры и градостроительства
- Кафедра архитектуры и ландшафта
- Кафедра архитектурного проектирования
- Кафедра градостроительства

#### Заочный факультет
- Учебная лаборатория электронного обучения и дистанционных образовательных технологий

#### Общеуниверситетские кафедры
- Кафедра высшей математики
- Кафедра физики
- Кафедра лингвистики
- Кафедра физического воспитания
- Кафедра истории, философии и социальных наук
- Военный учебный центр

    """
    
    # Шаг 1: Разделение документа на части
    sections = split_document(document)
    
    print(sections)
    
    # Шаг 2: Получение эмбеддингов для каждой части документа
    embeddings = [get_embeddings(section, url) for section in sections]
    
    # Шаг 3: Создание индекса FAISS
    index = create_faiss_index(embeddings)
    
    # Шаг 4: Пример поиска по запросу
    query = "Какие есть кафедры в МИИГАИК?"
    best_section = search_faiss(query, index, sections, url)
    
    print(f"Лучший ответ на запрос: \n{best_section}")


if __name__ == "__main__":
    main()


## ЗАГЛУШКА ###
def get_model_answer(text):
    return 'Привет! Меня зовут Гисик. Задавай любой вопрос!'
