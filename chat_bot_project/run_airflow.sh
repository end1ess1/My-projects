#!/bin/bash
cd $HOME && source airflow_env/bin/activate && cd "$AIRFLOW_HOME" && airflow scheduler
cd $HOME && source airflow_env/bin/activate && cd "$AIRFLOW_HOME" && airflow webserver

source airflow_env/bin/activate && cd "/mnt/c/Users/My End_1ess C/Documents/Диплом/MyGithub/end1ess1/chat_bot_project/Airflow/Scripts" && python3 telegram_bot.py


