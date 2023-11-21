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



## Contacts

If you got any question, feel free to contact us at [jeremyan@connect.hku.hk](mailto: jeremyan@connect.hku.hk)
