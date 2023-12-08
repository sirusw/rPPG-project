# 使用官方 Mosquitto 镜像作为基础镜像
FROM eclipse-mosquitto

# 复制自定义配置文件到容器内的 Mosquitto 配置目录
COPY ./mosquitto.conf /mosquitto/config/mosquitto.conf

# 暴露 MQTT 默认端口
EXPOSE 1883

# 运行 Mosquitto
CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
