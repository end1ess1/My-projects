import subprocess
from lib import Log, ModelArgs
from rich.traceback import install
from connection import connect_to_databases

install(show_locals=True)

def start_server():
    '''Функция для старта сервера с моделью'''

    # Логирование в Посгре и Редис
    logging = Log(*connect_to_databases(), script_name='start_model.py')

    logging.log('Получение аргументов из командной строки')

    args = ModelArgs.parse_base_args()

    llama_server_path = args.llama_server_path
    model_path = args.model_path
    host = args.host
    port = args.port
    ngl = args.ngl
    context_size = args.context_size

    logging.success('Аргументы успешно запарсились')

    logging.log('Формируем команду для запуска')

    command = [
        llama_server_path,
        "-m", model_path,
        "-ngl", ngl,
        "-c", context_size,
        "--host", host,
        "--port", port,
        "embeddings" # запуск в эмбеддинг режиме
    ]

    try:
        logging.log('Пробуем запустить сервер')
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        logging.success(f"Llama сервер запущен по адресу http://{host}:{port}")

    except FileNotFoundError:
        logging.error("Ошибка: Проверь путь к llama-server.exe.")
    except KeyboardInterrupt:
        logging.error("\nСервер остановлен пользователем.")
        process.terminate()
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")