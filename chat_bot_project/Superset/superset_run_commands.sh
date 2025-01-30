#!/bin/bash

# Отладка файлов
ls /app/pythonpath/

# Создаем админа
superset fab create-admin \
  --username admin \
  --password admin \
  --firstname Egor \
  --lastname Abashin \
  --email e_abashin@inbox.ru

# Обновляем БД
superset db upgrade

# Инициализируем
superset init

# Дашборд
superset import-assets --path /app/superset_dasboards

# Запускем сервера Superset
superset run -h 0.0.0.0 -p 8088
