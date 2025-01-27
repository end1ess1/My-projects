CREATE ROLE telegram_bot_db_not_owners; -- Роль для БД
GRANT telegram_bot_db_not_owners TO superset_admin, airflow_admin -- Добавили юзеров в роль
