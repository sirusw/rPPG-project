#!/bin/bash
# start.sh

# 启动 Django MQTT 客户端作为后台进程
python manage.py mqttclient &

# 启动 Daphne ASGI 应用
daphne server.asgi:application
