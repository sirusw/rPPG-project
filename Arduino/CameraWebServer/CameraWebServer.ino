#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiManager.h> // Include the Wi-Fi Manager library
#include <PubSubClient.h>
#include <EEPROM.h> // Include the EEPROM library to enable reading and writing to the flash memory
#include <base64.h>

//
// WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
//            Ensure ESP32 Wrover Module or other board with PSRAM is selected
//            Partial images will be transmitted if image exceeds buffer size
//
//            You must select partition scheme from the board menu that has at least 3MB APP space.
//            Face Recognition is DISABLED for ESP32 and ESP32-S2, because it takes up from 15 
//            seconds to process single frame. Face Detection is ENABLED if PSRAM is enabled as well

// ===================
// Select camera model
// ===================

#define CAMERA_MODEL_WROVER_KIT // Has PSRAM
// #define CAMERA_MODEL_ESP_EYE // Has PSRAM
//#define CAMERA_MODEL_ESP32S3_EYE // Has PSRAM
//#define CAMERA_MODEL_M5STACK_PSRAM // Has PSRAM
//#define CAMERA_MODEL_M5STACK_V2_PSRAM // M5Camera version B Has PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE // Has PSRAM
//#define CAMERA_MODEL_M5STACK_ESP32CAM // No PSRAM
//#define CAMERA_MODEL_M5STACK_UNITCAM // No PSRAM
//#define CAMERA_MODEL_AI_THINKER // Has PSRAM
//#define CAMERA_MODEL_TTGO_T_JOURNAL // No PSRAM
//#define CAMERA_MODEL_XIAO_ESP32S3 // Has PSRAM
// ** Espressif Internal Boards **
//#define CAMERA_MODEL_ESP32_CAM_BOARD
//#define CAMERA_MODEL_ESP32S2_CAM_BOARD
//#define CAMERA_MODEL_ESP32S3_CAM_LCD
//#define CAMERA_MODEL_DFRobot_FireBeetle2_ESP32S3 // Has PSRAM
//#define CAMERA_MODEL_DFRobot_Romeo_ESP32S3 // Has PSRAM
#include "camera_pins.h"

#define MQTT_MAX_PACKET_SIZE (256 * 1024)

// ===========================
// Enter your WiFi credentials
// ===========================
// const char* ssid = "SW";
// const char* password = "12345678";
// // MQTT Broker settings
// const char* mqtt_broker = "192.168.108.150";
// const int mqtt_port = 18839;
// const char* mqtt_username = "mqtt";
// const char* mqtt_password = "1234";

WiFiManager wifiManager;

// WiFiManagerParameter custom_mqtt_broker;
// WiFiManagerParameter custom_mqtt_username;
// WiFiManagerParameter custom_mqtt_password;
// WiFiManagerParameter custom_mqtt_port;
// WiFiManagerParameter custom_mqtt_tx;
// WiFiManagerParameter custom_mqtt_rx;

char wifi_ssid[32] = "SW";
char wifi_password[32] = "12345678";
char mqtt_broker[32] = "192.168.0.106";
char mqtt_username[32] = "mqtt";
char mqtt_password[32] = "1234";
char mqtt_tx[32] = "/data/tx";
char mqtt_rx[32] = "/data/rx";
int mqtt_port = 18839;

WiFiManagerParameter custom_mqtt_broker("broker", "MQTT broker", mqtt_broker, 32);
WiFiManagerParameter custom_mqtt_username("username", "MQTT username", mqtt_username, 32);
WiFiManagerParameter custom_mqtt_password("password", "MQTT password", mqtt_password, 32);
WiFiManagerParameter custom_mqtt_port("port", "MQTT port", String(mqtt_port).c_str(), 5);
WiFiManagerParameter custom_mqtt_tx("tx", "tx", mqtt_tx, 32);
WiFiManagerParameter custom_mqtt_rx("rx", "rx", mqtt_rx, 32);

WiFiClient espClient;
PubSubClient client(espClient);


void startCameraServer();
void setupLedFlash(int pin);

void saveConfigCallback () {
  Serial.println("Inside saveConfigCallback");
  String ssid = wifiManager.getWiFiSSID();
  String password = wifiManager.getWiFiPass();
  Serial.println(ssid); 
  Serial.println(password);
  strncpy(wifi_ssid, ssid.c_str(), sizeof(wifi_ssid));
  strncpy(wifi_password, password.c_str(), sizeof(wifi_password));

  strncpy(mqtt_broker, custom_mqtt_broker.getValue(), sizeof(mqtt_broker));
  strncpy(mqtt_username, custom_mqtt_username.getValue(), sizeof(mqtt_username));
  strncpy(mqtt_password, custom_mqtt_password.getValue(), sizeof(mqtt_password));
  mqtt_port = atoi(custom_mqtt_port.getValue());

  strncpy(mqtt_tx, custom_mqtt_tx.getValue(), sizeof(mqtt_tx));
  strncpy(mqtt_rx, custom_mqtt_rx.getValue(), sizeof(mqtt_rx));
  Serial.println("End of saveConfigCallback");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqtt_username, mqtt_password )) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_VGA;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  //config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 10;
  config.fb_count = 1;
  
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(config.pixel_format == PIXFORMAT_JPEG){
    if(psramFound()){
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      // Limit the frame size when PSRAM is not available
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    // Best option for face detection/recognition
    config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
    config.fb_count = 2;
#endif
  }

#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if(config.pixel_format == PIXFORMAT_JPEG){
    s->set_framesize(s, FRAMESIZE_QVGA);
  }

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

#if defined(CAMERA_MODEL_ESP32S3_EYE)
  s->set_vflip(s, 1);
#endif

// Setup LED FLash if LED pin is defined in camera_pins.h
#if defined(LED_GPIO_NUM)
  setupLedFlash(LED_GPIO_NUM);
#endif
  wifiManager.setConfigPortalTimeout(180); 
  wifiManager.setBreakAfterConfig(false);

  wifiManager.addParameter(&custom_mqtt_broker);
  wifiManager.addParameter(&custom_mqtt_username);
  wifiManager.addParameter(&custom_mqtt_password);
  wifiManager.addParameter(&custom_mqtt_port);
  wifiManager.addParameter(&custom_mqtt_tx);
  wifiManager.addParameter(&custom_mqtt_rx);

  wifiManager.setSaveConfigCallback(saveConfigCallback);

  // Uncomment for testing wifi manager
  //wifiManager.resetSettings();

  // Exit the configuration portal after trying to connect to Wi-Fi for a minute
  // wifiManager.setConfigPortalTimeout(240);

  // If it cannot connect to Wi-Fi in the given time, it starts an access point with the specified name
  // Here, "AutoConnectAP" is the name of the created Access Point
  // and goes into a blocking loop awaiting configuration
  if (!wifiManager.startConfigPortal("ESP32")) {
    Serial.println("Failed to connect and hit timeout");
    // // Reset and try again, or maybe put it to deep sleep
    // ESP.restart();
    // delay(1000);
  }
  else {
    Serial.println("Wifi: ");
    Serial.println(wifi_ssid);
    Serial.println("Pass: ");
    Serial.println(wifi_password);
    WiFi.begin(wifi_ssid, wifi_password);
    delay(1000);
    unsigned long startTime = millis();
    while(WiFi.status() != WL_CONNECTED) {
      if (millis() - startTime > 5000) {  // 5 second timeout
        Serial.println("Failed to connect to WiFi");
        break;
      }
      delay(1000);
    }
    if(WiFi.status() == WL_CONNECTED) {
      Serial.println("Connected to WiFi!");
    }
  }

  // WiFi.begin(wifi_ssid, wifi_password);

  // If you get here you have connected to the Wi-Fi
  Serial.println("Connected");

  // MQTT connection
  Serial.println("MQTT:");
  Serial.println("mqtt_broker");
  Serial.println("mqtt_port");
  Serial.println("mqtt_username");
  Serial.println("mqtt_password");
  Serial.println("MQTT:");
  // client.setBufferSize(MQTT_MAX_PACKET_SIZE); // increase from default 128 bytes
  client.setServer(mqtt_broker, mqtt_port);
  
  int connection_attempts = 0;
  while (!client.connected() && connection_attempts < 5) {
      if (client.connect("ESP32Client", mqtt_username, mqtt_password )) {
        Serial.println("Connected to MQTT Broker!");
        client.publish("/data/tx", "hello world");
      } else {
        Serial.println("Failed to connect to MQTT Broker.");
        delay(2000);
      }
      connection_attempts++;
  }

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  camera_fb_t * fb = NULL;

  // Capture a frame
  fb = esp_camera_fb_get();
  if(!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Convert the image data to Base64
  String image_data_base64 = base64::encode((uint8_t*)fb->buf, fb->len);

  // Publish the Base64 image data to a MQTT topic
  // Note: This might fail if the image data is too large. Most MQTT brokers
  // have a maximum packet size of around 256 kB.
  Serial.print("image length:");
  Serial.print(image_data_base64.length());
  if(image_data_base64.length() < MQTT_MAX_PACKET_SIZE){
    // Publish image
    int result = client.publish("/data/tx", image_data_base64.c_str());

    // Check result
    if (result == true) {
      Serial.println("Image sent");
    } else {
      Serial.print("Error sending image:");
      Serial.println(result);
    }
  } else {
    Serial.println("Image too large to send over MQTT");
  }

  // Return the frame buffer back to the driver for reuse
  esp_camera_fb_return(fb);
}


