# Переменные
NETWORK='apps_network'

Запускаем виртуальное окружение
source venv/Scripts/activate

# Удаление всех старых процессов
echo KILLING OLD DOCKER PROCESSES
docker-compose -f Databases/PostgreSQL/docker-compose.yml rm -fs
docker-compose -f Databases/Redis/docker-compose.yml rm -fs
docker-compose -f Superset/docker-compose.yml rm -fs

echo REMOVING NETWORK:
docker network rm -f $NETWORK
echo NETWORK LIST:
docker network ls

echo DELETING VOLUMES:
docker volume rm pgadmin-volume
docker volume rm postgres-volume
docker volume rm redis-volume
docker volume rm superset-volume

# Запускаем новые процессы
echo CREATING NETWORK:
docker network create $NETWORK
echo NETWORK LIST:
docker network ls

echo UP DOCKER CONTAINERS:
docker-compose -f Databases/PostgreSQL/docker-compose.yml up -d
docker-compose -f Databases/Redis/docker-compose.yml up -d

sleep 5

docker-compose -f Superset/docker-compose.yml build
docker-compose -f Superset/docker-compose.yml up -d

echo ACTIVE CONTAINERS LIST:
docker ps

# echo CONTAINERS RESOURCE STATISTIC:
# docker stats

echo RUNNING BOT:
cd "C:\Users\My End_1ess C\Documents\Диплом\MyGithub\end1ess1\chat_bot_project\Airflow\scripts"
python telegram_bot.py
