import requests

url = 'http://192.168.0.156:5000/completion'
prompt = "Привет! Расскажи о чем хочешь"

#chat_history = []

# def format_history(history):
#     return "\n".join([f"User: {q}\nAI: {a}" for q, a in history])
# context_prompt = format_history(chat_history) + f"\nUser: {prompt}\nAI:"
# Сделать сохранение в файл

# retrieved_context = search_documents(prompt)
# context = format_history(chat_history) + f"\n{retrieved_context}\nUser: {prompt}\nAI:"

def get_model_answer(prompt, url: str=url):
    # URL сервера llama.cpp (замени на свой адрес и порт)
    # url = "http://localhost:5000/completion"

    # Текст запроса (промпт)
    data = {
        "prompt": prompt, #"n_predict": 128,
        #"max_tokens": 100,  # Максимальное количество токенов в ответе
        #"temperature": 0.7,  # Параметр для вариативности ответов
        #"top_p": 0.9,  # Сэмплинг по вероятности
    }

    # Отправка POST-запроса на сервер
    response = requests.post(url, json=data)

    # Обработка ответа
    if response.status_code == 200:
        #print(response.json())
        print("Ответ от модели:", response.json().get("content"))
        return response.json().get("content")
    else:
        print("Ошибка:", response.status_code, response.text)
        return None

def get_model_answer(prompt, url: str=url):
    return 'Some Answer'