import subprocess
import faiss
import numpy as np
from transformers import LlamaTokenizer, LlamaForCausalLM
from rich.traceback import install
import torch

# Установить rich для красивых traceback
install(show_locals=True)

# Параметры запуска
llama_server_path = "path/to/llama-server.exe"  # Укажи путь к llama-server.exe
model_path = "../LLM/Gemma-2-9B-It-SPPO-Iter3-Q2_K.gguf"  # Путь к модели
host = "192.168.0.156"  # Хост
port = 5000  # Порт
ngl = 100  # Количество слоев GPU для ускорения
context_size = 2048  # Размер контекста

# Запуск Llama сервера
command = [
    llama_server_path,
    "-m", model_path,
    "-ngl", str(ngl),
    "-c", str(context_size),
    "--host", host,
    "--port", str(port),
]

def start_llama_server():
    try:
        # Запуск процесса
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Llama сервер запущен по адресу http://{host}:{port}")
        return process
    except FileNotFoundError:
        print("Ошибка: Проверь путь к llama-server.exe.")
    except Exception as e:
        print(f"Произошла ошибка при запуске сервера: {e}")

# Инструменты для работы с FAISS (индексация документа)
class DocumentRetrieval:
    def __init__(self, document_text):
        self.document_text = document_text
        self.index = self.build_index(document_text)
        self.tokenizer = LlamaTokenizer.from_pretrained("path/to/tokenizer")
        self.model = LlamaForCausalLM.from_pretrained("path/to/model")

    def build_index(self, document_text):
        # Преобразование документа в векторы
        sentences = document_text.split("\n")  # Разделяем на предложения
        embeddings = [self.tokenize_and_embed(sentence) for sentence in sentences]
        
        # FAISS индекс
        dim = len(embeddings[0])  # Размерность вектора
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings).astype(np.float32))
        return index

    def tokenize_and_embed(self, text):
        # Получение эмбеддингов текста (здесь placeholder для модели)
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs['input_ids'])
        return embeddings.mean(dim=1).numpy()  # Возвращаем усредненный вектор

    def retrieve(self, query, top_k=3):
        query_embedding = self.tokenize_and_embed(query)
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        return [self.document_text.split("\n")[i] for i in indices[0]]

# Функция для генерации ответа на основе извлеченной информации
def generate_answer(query, document):
    retrieval_system = DocumentRetrieval(document)
    relevant_texts = retrieval_system.retrieve(query)
    context = " ".join(relevant_texts)

    # Передаем контекст в модель для генерации ответа
    inputs = llama_tokenizer(context + query, return_tensors="pt", truncation=True, max_length=context_size)
    outputs = llama_model.generate(**inputs, max_length=100)

    answer = llama_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Пример документа
document = """
Правила подачи и рассмотрения апелляций по результатам вступительных испытаний, проводимых МИИГАиК самостоятельно
...
"""

# Пример запроса
query = "Какие сроки подачи апелляции по результатам письменного экзамена?"

# Запуск сервера Llama
process = start_llama_server()

# Генерация ответа
answer = generate_answer(query, document)
print(answer)
