import subprocess
from private_file import dict_params
from rich.traceback import install
install(show_locals=True)

#Args.parse

# llama_server_path = args.
# model_path = args.
# host = args.
# port = args.
# ngl = args.
# context_size = args.

# Параметры запуска
llama_server_path = "path/to/llama-server.exe"  # Укажи путь к llama-server.exe
model_path = "../LLM/Gemma-2-9B-It-SPPO-Iter3-Q2_K.gguf"  # Путь к модели
host = "192.168.0.156"  # Хост
port = 5000  # Порт
ngl = 100  # Количество слоев GPU для ускорения
context_size = 2048  # Размер контекста

# Формируем команду
command = [
    llama_server_path,
    "-m", model_path,
    "-ngl", str(ngl),
    "-c", str(context_size),
    "--host", host,
    "--port", str(port),
]

try:
    # Запуск процесса
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print(f"Llama сервер запущен по адресу http://{host}:{port}")
    print("Выход из программы с помощью CTRL+C")

    # Вывод логов
    for line in process.stdout:
        print(line, end="")

except FileNotFoundError:
    print("Ошибка: Проверь путь к llama-server.exe.")
except KeyboardInterrupt:
    print("\nСервер остановлен пользователем.")
    process.terminate()
except Exception as e:
    print(f"Произошла ошибка: {e}")