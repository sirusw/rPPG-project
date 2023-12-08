# ESP32 Camera-based Heart Rate Detection with rPPG
rPPG (remote photoplethysmography) is a technique that enables the measurement of heart rate and other vital signs remotely using a camera. In this project, we explore the implementation of rPPG using an ESP32-based camera module. By analyzing subtle changes in skin color caused by blood flow, we can detect heart rate without the need for physical contact. This opens up possibilities for non-invasive, contactless monitoring of vital signs in various applications, such as healthcare, fitness tracking, and biometric authentication.

## Requirements
- ESP32-CAM module
- Home WiFi or hotspot with 2.4GHz bandwidth

## Setup
Here are the steps to set up this project:

1. Power ESP32: Connect your ESP32 module to power. You may need to press the reset button on the module, depending on your specific module.

2. Connect to AP: On your computer or mobile device, connect to the WiFi network created by the ESP32. This network will be named "ESP32". A setup page from WiFiManager will pop up upon connection.

3. Configure WiFi: In the WiFi manager, configure the ESP32 to connect to your home WiFi or hotspot. Make sure the WiFi or hotspot is using a **2.4GHz** bandwidth. **Make sure the WiFi that you are trying to connect is detected, then click on the WiFi ssid, then enter the password**, if no WiFi is detected, tap "Refresh".

4. Save Configuration: Click "save" in the WiFi manager to save your settings.

Please note that the WiFi manager configuration may fail on the first attempt, causing the AP to restart. If this happens, repeat the above steps.

## Deploy
英语不好先用中文，之后帮我翻译成英文
除了Arduino部分外，其他部分都是在Ubuntu虚拟机上容器化部署。
原理是运行docker-compose编排文件时，它会自动构建镜像，然后运行镜像。

0、请确保虚拟机的防火墙关了，因为很碍事。

sudo ufw disable

1、安装docker和docker-compose

sudo apt update

sudo apt install docker.io

2、为了日后方便，可以设置docker服务开机自启

sudo systemctl start docker

sudo systemctl enable docker

3、安装docker-compose

sudo curl -L "https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

#验证 Docker Compose 是否正确安装，成功会显示出安装的 Docker Compose 版本。

docker-compose --version 

4、把Docker Compose 会在后台启动服务，并且命令行不会被挂起显示容器的输出信息。

docker-compose up -d

5、停止rPPG系统

docker-compose down -v

ps：如果系统感觉不通，可以用在本地CMD中telnet自己虚拟机的端口排查

telnet  <虚拟机ip>  <port>


## Contacts

If you got any question, feel free to contact us at [jeremyan@connect.hku.hk](mailto: jeremyan@connect.hku.hk)
