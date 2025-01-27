import os
import json

with open("/app/pythonpath/redis_db_mapping.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Инфо по БД
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

# Подключение к БД
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_NAME}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

PRESET_DATABASES = {
    "PostgreSQL": {
        "name": "POSTGRES DB",
        "sqlalchemy_uri": SQLALCHEMY_DATABASE_URI,
        "extra": '{"engine_params": {"connect_args": {"options": "-c timezone=utc"}}}'
    }
}

# Инфо по Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = data["redis_db"]["superset"]

# Кеширование в Redis
DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_DB,
}
