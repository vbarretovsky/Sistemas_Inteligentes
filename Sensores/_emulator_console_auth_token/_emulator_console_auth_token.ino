#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "dht.h"
#include <Wire.h>
#include <BH1750.h>

#define dht_apin D5

ESP8266WiFiMulti WiFiMulti;
BH1750 lightMeter;
dht DHT;

void setup() {

  Serial.begin(115200);
  // Serial.setDebugOutput(true);
  Wire.begin(D2,D1);
  lightMeter.begin();
  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("NOS-F02D", "J7LC5G4C");

}

void loop() {
 DHT.read11(dht_apin); //Leitura do sensor de temperatura e humidade
 String hum = String(DHT.humidity);
 String temperature = String(DHT.temperature);
 String lux = String(lightMeter.readLightLevel()); //LEITURA DO SENSOR DE LUZ
 Serial.print("Humidade e igual a:");
 Serial.print(hum);
  
  
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, "http://emoncms.org/input/post?node=emontx&fulljson={\"temperature\":"+temperature+",\"Humidity\":"+hum+",\"Luz\":"+lux+"}&apikey=6ddc3cc5b9ffd1771cf50106ad3388c4")) {  // HTTP


      Serial.print("[HTTP] GET...\n");
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }

  delay(10000);
}
