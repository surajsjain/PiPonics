#include <Firmata.h>
#include <FirmataMarshaller.h>
#include <FirmataDefines.h>
#include <FirmataParser.h>
#include <Boards.h>
#include <FirmataConstants.h>

#include <ArduinoJson.h>
#include <Ethernet.h>
#include <SPI.h>
#include <dht.h>

dht DHT;
#define DHT11_PIN 3

int soilSensorPin = A0;
int sensorValue;
int limit = 300;


EthernetClient client;

// Replace with your Raspberry Pi IP address
const char* server = "speeve-ponics.herokuapp.com";

// Replace with your server port number frequently port 80 - with Node-RED you need to use port 1880
int portNumber = 80;

// Replace with your unique URL resource
const char* resource = "/conditions/plant";

const unsigned long HTTP_TIMEOUT = 10000;  // max respone time from server
const size_t MAX_CONTENT_SIZE = 512;       // max size of the HTTP response

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

// ARDUINO entry point #1: runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;  // wait for serial port to initialize
  }
  Serial.println("Serial ready");
  if (!Ethernet.begin(mac)) {
    Serial.println("Failed to configure Ethernet");
    return;
  }
  Serial.println("Ethernet ready");
  delay(1000);
}



// ARDUINO entry point #2: runs over and over again forever
void loop() {
  if (connect(server, portNumber)) {
    if (sendRequest(server, resource) && skipResponseHeaders()) {
      Serial.print("HTTP POST request finished.");
    }
  }
  disconnect();
  wait();
}



// Open connection to the HTTP server (Node-RED running on Raspberry Pi)
bool connect(const char* hostName, int portNumber) {
  Serial.print("Connect to ");
  Serial.println(hostName);

  bool ok = client.connect(hostName, portNumber);

  Serial.println(ok ? "Connected" : "Connection Failed!");
  return ok;
}

// Send the HTTP POST request to the server
bool sendRequest(const char* host, const char* resource) {
  // Reserve memory space for your JSON data
  StaticJsonBuffer<200> jsonBuffer;

  // Build your own object tree in memory to store the data you want to send in the request
  JsonObject& root = jsonBuffer.createObject();
  root["plant"] = 1;
  root["temperature"] = getTemperature();
  root["humidity"] = getHumidity();
  root["soilMoisture"] = 72.0;
  root["diseased"] = false;

  // Generate the JSON string
  root.printTo(Serial);

  Serial.print("POST ");
  Serial.println(resource);

  client.print("POST ");
  client.print(resource);
  client.println(" HTTP/1.1");
  client.print("Host: ");
  client.println(host);
  client.println("Connection: close\r\nContent-Type: application/json");
  client.print("Content-Length: ");
  client.print(root.measureLength());
  client.print("\r\n");
  client.println();
  root.printTo(client);

  return true;
}

bool skipResponseHeaders() {
  // HTTP headers end with an empty line
  char endOfHeaders[] = "\r\n\r\n";

  client.setTimeout(HTTP_TIMEOUT);
  bool ok = client.find(endOfHeaders);

  if (!ok) {
    Serial.println("No response or invalid response!");
  }
  return ok;
}

void disconnect() {
  Serial.println("Disconnect");
  client.stop();
}

void wait() {
  Serial.println("Wait 15 minutes");
  delay(15 * 60000);
}

int getTemperature()
{
  int chk = DHT.read11(DHT11_PIN);
  int temp = (int)(DHT.temperature);

  return (temp);
}

int getHumidity()
{
  int chk = DHT.read11(DHT11_PIN);
  int hum = (int)(DHT.humidity);

  return (hum);
}

boolean getSoilMoisture()
{
  sensorValue = analogRead(soilSensorPin);
  if (sensorValue < limit) {
    return (true);
  }
  else {
    return (false);
  }
  delay(1000);
}
