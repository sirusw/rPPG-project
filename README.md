# ESP32 Camera Project with MQTT
This project uses an ESP32-CAM module to capture and send video frames to an MQTT broker. The ESP32-CAM is a small-sized camera module that combines a 2MP camera, microSD card slot, and a microcontroller in one package. MQTT is a lightweight messaging protocol for small sensors and mobile devices.

## Requirements
- ESP32-CAM module
- MQTT broker
- Home WiFi or hotspot with 2.4GHz bandwidth
## Setup
Here are the steps to set up this project:

1. Check IPv4 Address: Use the ipconfig command on your computer to find your IPv4 address.

2. Configure Mosquitto: Open your mosquitto.conf file and set the address to your IPv4 address and the port to 18839.

3. Set MQTT Credentials: The MQTT username is "mqtt" and the password is "1234".

4. Power ESP32: Connect your ESP32 module to power. You may need to press the reset button on the module, depending on your specific module.

5. Connect to AP: On your computer or mobile device, connect to the WiFi network created by the ESP32. This network will be named "ESP32". A setup page from WiFiManager will pop up upon connection.

6. Configure WiFi: In the WiFi manager, configure the ESP32 to connect to your home WiFi or hotspot. Make sure the WiFi or hotspot is using a 2.4GHz bandwidth.

7. Configure MQTT Broker IP: In the WiFi manager, enter the IP address of your MQTT broker.

8. Save Configuration: Click "save" in the WiFi manager to save your settings.

Please note that the WiFi manager configuration may fail on the first attempt, causing the AP to restart. If this happens, simply repeat the above steps.



## Contacts

If you got any question, feel free to contact us at [jeremyan@connect.hku.hk](mailto: jeremyan@connect.hku.hk)
