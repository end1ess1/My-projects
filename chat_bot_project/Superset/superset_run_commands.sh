#!/bin/bash

# Создание администратора Superset
superset fab create-admin \
  --username admin \
  --password admin \
  --firstname Egor \
  --lastname Abashin \
  --email e_abashin@inbox.ru

# Обновление базы данных Superset
superset db upgrade

# Инициализация Superset
superset init

# Обновление системных пакетов
apt-get update

# Установка необходимых библиотек для работы с PosgtreSQL
apt-get install -y gcc libpq-dev

# Установка модуля psycopg2
pip install psycopg2

# Запуск сервера Superset
superset run -h 0.0.0.0 -p 8088