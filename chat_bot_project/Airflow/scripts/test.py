import requests
from rich.traceback import install
from requests.auth import HTTPBasicAuth
install(show_locals=True)
# Параметры подключения
sqlalchemy_uri = "postgresql://admin:admin@postgres:5432/preprod_db"
database_name = "Postgres Preprod DB"
superset_url = "http://localhost:8088"  # Замените на ваш адрес
username = "admin"  # Замените на имя пользователя для доступа
password = "admin"  # Замените на пароль

# Логинимся
auth = HTTPBasicAuth(username, password)
login_url = f"{superset_url}/api/v1/security/login"
login_payload = {"username": username, "password": password, "provider": "db", "refresh": True}
session = requests.Session()
session.post(login_url, json=login_payload, auth=auth)

# Добавляем базу данных
database_url = f"{superset_url}/api/v1/database"
database_payload = {
    "database_name": database_name,
    "sqlalchemy_uri": sqlalchemy_uri,
}
headers = {"Content-Type": "application/json"}

response = session.post(database_url, json=database_payload, headers=headers)

if response.status_code == 200:
    print("Database added successfully!")
else:
    print(f"Failed to add database: {response.text}")