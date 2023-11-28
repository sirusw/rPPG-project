#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiManager.h>  // Include the Wi-Fi Manager library
#include <PubSubClient.h>
#include <EEPROM.h>  // Include the EEPROM library to enable reading and writing to the flash memory
#include <base64.h>
#include <ArduinoJson.h>
#include <Preferences.h>
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

#define CAMERA_MODEL_WROVER_KIT  // Has PSRAM
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

#define MQTT_MAX_PACKET_SIZE 100000

WiFiManager wifiManager;

char wifi_ssid[32] = "TP-Link_920A";
char wifi_password[32] = "59900368";
char mqtt_broker[32] = "192.168.0.103";
int mqtt_port = 18839;
char mqtt_username[32] = "mqtt";
char mqtt_password[32] = "1234";
char mqtt_tx[32] = "/data/tx";
char mqtt_rx[32] = "/data/rx";

Preferences preferences;

WiFiManagerParameter custom_mqtt_broker("mqtt_broker", "mqtt broker", mqtt_broker, 40);

WiFiClient espClient;
PubSubClient client(espClient);


void startCameraServer();
void setupLedFlash(int pin);

void saveConfigCallback() {
  Serial.println("Inside saveConfigCallback");
  String ssid = wifiManager.getWiFiSSID();
  String password = wifiManager.getWiFiPass();
  
  Serial.println(ssid);
  Serial.println(password);
  strncpy(wifi_ssid, ssid.c_str(), sizeof(wifi_ssid));
  strncpy(wifi_password, password.c_str(), sizeof(wifi_password));
  String brokerValue = custom_mqtt_broker.getValue();  // Use the custom parameter directly
  strncpy(mqtt_broker, brokerValue.c_str(), sizeof(mqtt_broker));

  preferences.begin("my-app", false);
  preferences.putString("ssid", ssid);
  preferences.putString("password", password);
  preferences.putString("broker", brokerValue);
  preferences.end();

  Serial.println("End of saveConfigCallback");
}

void mqtt_config_callback(char* topic, byte* payload, unsigned int length) {

  // Parse JSON 
  payload[length] = '\0';
  String message = String((char*)payload);
  
  // Parse JSON
  const size_t capacity = JSON_OBJECT_SIZE(2) + 30;
  DynamicJsonDocument doc(capacity);
  deserializeJson(doc, message);

  // Get parameters
  const char* param = doc["param"];
  int value = doc["value"];
  
  sensor_t *s = esp_camera_sensor_get();

  Serial.println(param);
  Serial.println(value);

  if (strcmp(param, "sync") == 0) {

    sensor_t * s = esp_camera_sensor_get();
    
    DynamicJsonDocument syncDoc(2048);

    JsonArray params = syncDoc.createNestedArray("params");
    
    JsonObject paramObj;

    // Frame size
    paramObj = params.createNestedObject();
    paramObj["param"] = "framesize";
    paramObj["value"] = s->status.framesize;
    

    // Image quality
    paramObj = params.createNestedObject();
    paramObj["param"] = "quality";
    paramObj["value"] = s->status.quality;
    

    // Brightness 
    paramObj = params.createNestedObject();
    paramObj["param"] = "brightness";
    paramObj["value"] = s->status.brightness;
    
    
    // Contrast
    paramObj = params.createNestedObject();
    paramObj["param"] = "contrast";
    paramObj["value"] = s->status.contrast;
    
    
    // Saturation
    paramObj = params.createNestedObject();
    paramObj["param"] = "saturation";
    paramObj["value"] = s->status.saturation;
      

    // Gain ceiling
    paramObj = params.createNestedObject();
    paramObj["param"] = "gainceiling";
    paramObj["value"] = s->status.gainceiling;
    

    // Color bar  
    paramObj = params.createNestedObject();
    paramObj["param"] = "colorbar";
    paramObj["value"] = s->status.colorbar;
    

    // Automatic white balance
    paramObj = params.createNestedObject();
    paramObj["param"] = "awb";
    paramObj["value"] = s->status.awb;
    

    // Auto gain control
    paramObj = params.createNestedObject();
    paramObj["param"] = "agc";
    paramObj["value"] = s->status.agc;
    

    // Auto exposure
    paramObj = params.createNestedObject();
    paramObj["param"] = "aec";
    paramObj["value"] = s->status.aec;
    

    // Horizontal flip
    paramObj = params.createNestedObject();
    paramObj["param"] = "hmirror";
    paramObj["value"] = s->status.hmirror;
    
    
    // Vertical flip
    paramObj = params.createNestedObject();
    paramObj["param"] = "vflip";
    paramObj["value"] = s->status.vflip;
    

    // AWB gain
    paramObj = params.createNestedObject();
    paramObj["param"] = "awb_gain";
    paramObj["value"] = s->status.awb_gain;
    

    // AGC gain
    paramObj = params.createNestedObject();
    paramObj["param"] = "agc_gain";
    paramObj["value"] = s->status.agc_gain;
    

    // AEC value
    paramObj = params.createNestedObject();
    paramObj["param"] = "aec_value";
    paramObj["value"] = s->status.aec_value;
    

    // AEC2
    paramObj = params.createNestedObject();
    paramObj["param"] = "aec2";
    paramObj["value"] = s->status.aec2;
    

    // DCW
    paramObj = params.createNestedObject();
    paramObj["param"] = "dcw";
    paramObj["value"] = s->status.dcw;
    

    // BPC
    paramObj = params.createNestedObject();
    paramObj["param"] = "bpc";
    paramObj["value"] = s->status.bpc;
    

    // WPC
    paramObj = params.createNestedObject();
    paramObj["param"] = "wpc";
    paramObj["value"] = s->status.wpc;
    

    // Raw GMA
    paramObj = params.createNestedObject();
    paramObj["param"] = "raw_gma";
    paramObj["value"] = s->status.raw_gma;
    

    // Lens correction
    paramObj = params.createNestedObject();
    paramObj["param"] = "lenc";
    paramObj["value"] = s->status.lenc;
    

    // Special effects
    paramObj = params.createNestedObject();
    paramObj["param"] = "special_effect";
    paramObj["value"] = s->status.special_effect;
    

    // WB mode
    paramObj = params.createNestedObject();
    paramObj["param"] = "wb_mode";
    paramObj["value"] = s->status.wb_mode;
    

    // AE level
    paramObj = params.createNestedObject();
    paramObj["param"] = "ae_level";
    paramObj["value"] = s->status.ae_level;  
    

    char buffer[2048];
    serializeJson(syncDoc, buffer);
    
    client.publish("/config/tx", buffer);
    
  }
  else if (strcmp(param, "framesize") == 0) {
    framesize_t val = (framesize_t)value;
    if (s->pixformat == PIXFORMAT_JPEG) {
      s->set_framesize(s, val); 
    }
  } 
  else if (strcmp(param, "quality") == 0) {
    s->set_quality(s, value);
  }
  else if (strcmp(param, "contrast") == 0) {
    s->set_contrast(s, value);
  }
  else if (strcmp(param, "brightness") == 0) {
    s->set_brightness(s, value);
  }
  else if (strcmp(param, "saturation") == 0) {
    s->set_saturation(s, value);  
  }
  else if (strcmp(param, "gainceiling") == 0) {
    s->set_gainceiling(s, (gainceiling_t)value);
  }
  else if (strcmp(param, "colorbar") == 0) {
    s->set_colorbar(s, value);
  }
  else if (strcmp(param, "awb") == 0) {
    s->set_whitebal(s, value);
  }
  else if (strcmp(param, "agc") == 0) {
    s->set_gain_ctrl(s, value);
  }
  else if (strcmp(param, "aec") == 0) {
    s->set_exposure_ctrl(s, value);
  }
  else if (strcmp(param, "hmirror") == 0) {
    s->set_hmirror(s, value);
  }
  else if (strcmp(param, "vflip") == 0) {
    s->set_vflip(s, value);
  }
  else if (strcmp(param, "awb_gain") == 0) {
    s->set_awb_gain(s, value);
  }
  else if (strcmp(param, "agc_gain") == 0) {
    s->set_agc_gain(s, value);
  }
  else if (strcmp(param, "aec_value") == 0) {
    s->set_aec_value(s, value);
  }
  else if (strcmp(param, "aec2") == 0) {
    s->set_aec2(s, value);
  }
  else if (strcmp(param, "dcw") == 0) {
    s->set_dcw(s, value);
  }
  else if (strcmp(param, "bpc") == 0) {
    s->set_bpc(s, value);
  }
  else if (strcmp(param, "wpc") == 0) {
    s->set_wpc(s, value);
  }
  else if (strcmp(param, "raw_gma") == 0) {
    s->set_raw_gma(s, value);
  }
  else if (strcmp(param, "lenc") == 0) {
    s->set_lenc(s, value);
  }
  else if (strcmp(param, "special_effect") == 0) {
    s->set_special_effect(s, value);
  }
  else if (strcmp(param, "wb_mode") == 0) {
    s->set_wb_mode(s, value);
  }
  else if (strcmp(param, "ae_level") == 0) {
    s->set_ae_level(s, value);
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqtt_username, mqtt_password)) {
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
  config.pixel_format = PIXFORMAT_JPEG;  // for streaming
  //config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 10;
  config.fb_count = 1;

  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if (config.pixel_format == PIXFORMAT_JPEG) {
    if (psramFound()) {
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

  sensor_t* s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1);        // flip it back
    s->set_brightness(s, 1);   // up the brightness just a bit
    s->set_saturation(s, -2);  // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if (config.pixel_format == PIXFORMAT_JPEG) {
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
  wifiManager.addParameter(&custom_mqtt_broker);

  wifiManager.setConfigPortalTimeout(180);
  wifiManager.setBreakAfterConfig(false);
  wifiManager.setSaveConfigCallback(saveConfigCallback);

  preferences.begin("my-app", true);
  String ssid = preferences.getString("ssid", "");
  String password = preferences.getString("password", "");
  String broker = preferences.getString("broker", "");
  preferences.end();

  // Copy to global variables
  strncpy(wifi_ssid, ssid.c_str(), sizeof(wifi_ssid));
  strncpy(wifi_password, password.c_str(), sizeof(wifi_password));
  strncpy(mqtt_broker, broker.c_str(), sizeof(mqtt_broker));

  WiFi.begin(wifi_ssid, wifi_password);
  delay(1000);
  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime > 5000) {  // 5 second timeout
      Serial.println("Failed to connect to WiFi");
      break;
    }
    delay(1000);
  }

  // client.setBufferSize(MQTT_MAX_PACKET_SIZE); // increase from default 128 bytes
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(mqtt_config_callback);

    bool mqttConnected = false;

    int connection_attempts = 0;
    while (!client.connected() && connection_attempts < 3) {
      if (client.connect("ESP32Client", mqtt_username, mqtt_password)) {
        Serial.println("Connected to MQTT Broker!");
        client.publish("/data/tx", "hello world");
        client.subscribe("/config/rx", 1);
        mqttConnected = true;
      } else {
        Serial.println("Failed to connect to MQTT Broker.");
        delay(1000);
      }
      connection_attempts++;
    }

  if (WiFi.status() == WL_CONNECTED && mqttConnected) {
    Serial.println("Connected to WiFi and MQTT!");
    
  } else {
    if (!wifiManager.startConfigPortal("ESP32")) {
      Serial.println("Failed to connect and hit timeout");
      // // Reset and try again, or maybe put it to deep sleep
      // ESP.restart();
      // delay(1000);
    } else {
      Serial.println("Wifi: ");
      Serial.println(wifi_ssid);
      Serial.println("Pass: ");
      Serial.println(wifi_password);
      WiFi.begin(wifi_ssid, wifi_password);
      delay(1000);
      unsigned long startTime = millis();
      while (WiFi.status() != WL_CONNECTED) {
        if (millis() - startTime > 5000) {  // 5 second timeout
          Serial.println("Failed to connect to WiFi");
          break;
        }
        delay(1000);
      }
      if (WiFi.status() == WL_CONNECTED) {
        Serial.println("Connected to WiFi!");
      }
    }
  }

  // WiFi.begin(wifi_ssid, wifi_password);

  // If you get here you have connected to the Wi-Fi
  Serial.println("Connected");

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

  camera_fb_t* fb = NULL;

  // Capture a frame
  fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Convert the image data to Base64
  String image_data_base64 = base64::encode((uint8_t*)fb->buf, fb->len);

  // Publish the Base64 image data to a MQTT topic
  // Note: This might fail if the image data is too large. Most MQTT brokers
  // have a maximum packet size of around 256 kB.
  // Serial.print("image length:");
  // Serial.print(image_data_base64.length());
  if (image_data_base64.length() < MQTT_MAX_PACKET_SIZE) {
    // Publish image
    int result = client.publish("/data/tx", image_data_base64.c_str());
    // int result = client.publish("data/tx", "hello!!");

    // Check result
    if (result == true) {
      // Serial.println("Image sent");
    } else {
      Serial.print("Error sending image:");
      Serial.println(result);
    }
  } else {
    Serial.println("Image too large to send over MQTT");
  }

  // Return the frame buffer back to the driver for reuse
  esp_camera_fb_return(fb);

  client.loop();
}
