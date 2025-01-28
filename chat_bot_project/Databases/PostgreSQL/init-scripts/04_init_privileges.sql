-- Отключаем подключение по умолчанию для всех бд
REVOKE CONNECT ON DATABASE superset_db FROM PUBLIC;
REVOKE CONNECT ON DATABASE airflow_db FROM PUBLIC;
REVOKE CONNECT ON DATABASE telegram_bot_db FROM PUBLIC;

-- Убираем все привилегии для других юзеров на уровне БД
REVOKE ALL ON DATABASE superset_db FROM airflow_admin;
REVOKE ALL ON DATABASE superset_db FROM telegram_bot_admin;

REVOKE ALL ON DATABASE airflow_db FROM superset_admin;
REVOKE ALL ON DATABASE airflow_db FROM telegram_bot_admin;

REVOKE ALL ON DATABASE telegram_bot_db FROM superset_admin;
REVOKE ALL ON DATABASE telegram_bot_db FROM airflow_admin;

-- Разрешаем подключение только владельцам БД
GRANT CONNECT ON DATABASE superset_db TO superset_admin;
GRANT CONNECT ON DATABASE airflow_db TO airflow_admin;
GRANT CONNECT ON DATABASE telegram_bot_db TO telegram_bot_admin;

-- Добавляем владельцам полные привилегии на БД
GRANT ALL PRIVILEGES ON DATABASE superset_db TO superset_admin;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_admin;
GRANT ALL PRIVILEGES ON DATABASE telegram_bot_db TO telegram_bot_admin;

GRANT USAGE ON SCHEMA public TO telegram_bot_admin;
GRANT CREATE ON SCHEMA public TO telegram_bot_admin;