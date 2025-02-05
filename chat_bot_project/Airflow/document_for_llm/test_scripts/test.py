import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Доки имеют четкую структуру и иерархию

def split_rules(text):
    # Попробуем исправить регулярку для поиска заголовков
    sections = re.split(r'(?=\n[IVXLCDM]+\.\s)', text)  # Пример исправленного регулярного выражения

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        separators=["\n\\d+\\. ", "\n\\s*[а-г]\\)", "\n\\s*- "]  # Экранируем специальные символы
    )
    
    chunks = []
    for section in sections:
        if section.strip():
            # Добавляем заголовок раздела как префикс
            header = re.search(r'^(.*?)\n', section).group(1) if re.search(r'^[IVXLCDM]+\.', section) else ""
            section_chunks = splitter.split_text(section)
            chunks.extend([f"РАЗДЕЛ: {header}\n{chunk}" for chunk in section_chunks])
            print(chunks)
    
    return chunks



legal_terms = {
    "МИИГАиК": "Московский государственный университет геодезии и картографии",
    "ФЗ №273": "Федеральный закон 'Об образовании в Российской Федерации'",
    "ГИА": "Государственная итоговая аттестация"
}

def normalize_terms(text):
    for term, expansion in legal_terms.items():
        text = re.sub(rf'\b{term}\b', f"{term} ({expansion})", text, flags=re.IGNORECASE)
    return text


def add_metadata(chunk, source_file):
    # Автоматическое определение типа информации
    category = "общие правила" if "общие положения" in chunk.lower() else \
               "квоты" if "квота" in chunk.lower() else \
               "документы" if "документ об образовании" in chunk.lower() else "другое"
    
    return {
        "text": chunk,
        "metadata": {
            "source": source_file,
            "category": category,
            "year": 2025,
            "section": re.search(r'РАЗДЕЛ: (.*?)\n', chunk).group(1) if "РАЗДЕЛ:" in chunk else None
        }
    }
    
def preprocess_text(text):
    # Удаление лишних пробелов и спецсимволов
    text = ' '.join(text.split())
    # Приведение к нижнему регистру (опционально)
    text = text.lower()  
    # Удаление символов, не входящих в ASCII (настраивайте под свои нужды)
    text = text.encode('ascii', 'ignore').decode()  
    return text
    
def process_admission_docs(file_path):
    # Чтение файла
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Предобработка
    text = preprocess_text(text)
    text = normalize_terms(text)
    
    # Разбиение на чанки
    chunks = split_rules(text)
    
    # Добавление метаданных
    return [add_metadata(chunk, file_path) for chunk in chunks]

process_admission_docs(r"C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\document_for_llm\main.txt")
