REVOKE CONNECT ON DATABASE superset_db FROM PUBLIC; -- запрещаем подключаться к бд

REVOKE CONNECT ON DATABASE airflow_db FROM PUBLIC;

REVOKE ALL ON DATABASE superset_db FROM airflow_admin; -- удаляем всевозможные привилегии на уровне бд
REVOKE ALL ON DATABASE superset_db FROM telegram_bot_admin;

REVOKE ALL ON DATABASE airflow_db FROM superset_admin;
REVOKE ALL ON DATABASE airflow_db FROM telegram_bot_admin;

GRANT CONNECT ON DATABASE superset_db TO superset_admin; -- доступ только нужным пользователям подключение к бд
GRANT CONNECT ON DATABASE airflow_db TO airflow_admin;
GRANT CONNECT ON DATABASE telegram_bot_db TO telegram_bot_db_not_owners;


GRANT ALL PRIVILEGES ON DATABASE telegram_bot_db TO telegram_bot_db_not_owners; -- добавляем группе пользователей все привелегии



GRANT CONNECT ON DATABASE telegram_bot_db TO telegram_bot_db_not_owners;
REVOKE ALL ON SCHEMA public FROM telegram_bot_db_not_owners;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM telegram_bot_db_not_owners;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM telegram_bot_db_not_owners;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM telegram_bot_db_not_owners;
REVOKE CREATE ON SCHEMA public FROM telegram_bot_db_not_owners;