# Переменные
NETWORK='apps_network'

# Запускаем виртуальное окружение
# source venv/Scripts/activate

# Удаление всех старых процессов
echo killing old docker processes
docker-compose -f Databases/PostgreSQL/docker-compose.yml rm -fs
docker-compose -f Databases/Redis/docker-compose.yml rm -fs
docker-compose -f Superset/docker-compose.yml rm -fs
docker-compose -f Airfow/docker-compose.yml rm -fs
Airflow>docker-compose up airflow-init


echo removing network
docker network rm -f $NETWORK
docker network ls

# Запускаем новые процессы
echo creating network
docker network create $NETWORK
docker network ls

echo up docker containers
docker-compose -f Databases/PostgreSQL/docker-compose.yml up -d
docker-compose -f Databases/Redis/docker-compose.yml up -d

docker-compose -f Superset/docker-compose.yml build
docker-compose -f Superset/docker-compose.yml up -d

docker-compose -f Airfow/docker-compose.yml up airflow-init -d
docker-compose -f Airfow/docker-compose.yml up -d

echo Active containers:
docker ps

# Предотвращаем закрытие интерактивной сессии
exec sh 


#docker-compose -f Airflow/docker-compose.yml rm -fs
#docker-compose -f Airflow/docker-compose.yml up -d