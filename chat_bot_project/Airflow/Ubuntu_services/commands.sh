sudo nano /etc/systemd/system/telegram_bot.service

# [Unit]
# Description=Telegram Bot Service
# After=network.target

# [Service]
# User=egor
# WorkingDirectory=/home/egor
# ExecStart=/bin/bash -c 'command'
# Restart=always
# RestartSec=5

# [Install]
# WantedBy=multi-user.target

sudo systemctl daemon-reload # для того чтобы увидел службу

sudo systemctl start telegram_bot.service
sudo systemctl stop telegram_bot.service
sudo systemctl status telegram_bot.service

journalctl -u telegram_bot.service # logs