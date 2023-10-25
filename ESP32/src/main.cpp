/*
 *  This sketch sends a message to a TCP server
 *
 */

#include <WiFi.h>
#include <WiFiMulti.h>
#include "pb_encode.h"
#include "pb_decode.h"
#include "proto/AppGetHistPower.pb.h"
#include "CRC16.h"


WiFiMulti WiFiMulti;
CRC16 crc;


// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

void setup()
{
    Serial.begin(9600);
    delay(10);

    // We start by connecting to a WiFi network
    WiFiMulti.addAP("<--ssid-->", "<--password-->");

    Serial.println();
    Serial.println();
    Serial.print("Waiting for WiFi... ");

    while(WiFiMulti.run() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    const char* ntpServer = "pool.ntp.org";
    configTime(0, 0, ntpServer);
    Serial.print("Epoch Time: ");
    Serial.println(getTime());

    crc.setInitial(CRC16_MODBUS_INITIAL);
    crc.setPolynome(CRC16_MODBUS_POLYNOME);
    crc.setReverseIn(CRC16_MODBUS_REV_IN);
    crc.setReverseOut(CRC16_MODBUS_REV_OUT);
    crc.setXorOut(CRC16_MODBUS_XOR_OUT);
    crc.restart();

    delay(500);
}

void readResponse(WiFiClient *client){
  unsigned long timeout = millis();
  while(client->available() == 0){
    if(millis() - timeout > 5000){
      Serial.println(">>> Client Timeout !");
      client->stop();
      return;
    }
  }

  // Read all the bytes of the reply from server and print them to Serial
  uint8_t buffer[1024];
  size_t read  = 0;
  while(client->available()) {
    buffer[read++] = client->read();
  }
  
  //Serial.printf("Response: ");
  //for(int i = 0; i<read; i++){
  //  Serial.printf("%02X",buffer[i]);
  //}  

  pb_istream_t istream;
  istream = pb_istream_from_buffer(buffer+10, read-10);

  AppGetHistPowerReqDTO appgethistpowerreqdto = AppGetHistPowerReqDTO_init_default;
  pb_decode(&istream, &AppGetHistPowerReqDTO_msg, &appgethistpowerreqdto);
  Serial.printf("sn: %lld, r_p: %i, et: %i, ed: %i\n", appgethistpowerreqdto.sn,appgethistpowerreqdto.r_p,appgethistpowerreqdto.et,appgethistpowerreqdto.ed);
}

void loop()
{
  const uint16_t port = 10081;
  const char * host = "192.168.1.203";

  uint8_t buffer[200];
  pb_ostream_t stream = pb_ostream_from_buffer(buffer, sizeof(buffer));
  AppGetHistPowerResDTO appgethistpowerres = AppGetHistPowerResDTO_init_default;
  appgethistpowerres.oft = 28800;
  appgethistpowerres.time = getTime();
  bool status = pb_encode(&stream, AppGetHistPowerResDTO_fields, &appgethistpowerres);

  if (!status)
  {
      Serial.println("Failed to encode");
      return;
  }

  for(int i = 0; i<stream.bytes_written; i++){
    //Serial.printf("%02X",buffer[i]);
    crc.add(buffer[i]);
  }  

  uint8_t header[10];
  header[0] = 0x48;
  header[1] = 0x4d;
  header[2] = 0xa3;
  header[3] = 0x15;
  header[4] = 0x00;
  header[5] = 0x01;
  header[6] = (crc.calc() >> 8) & 0xFF;
  header[7] = (crc.calc()) & 0xFF;
  header[8] = (stream.bytes_written+10 >> 8) & 0xFF;
  header[9] = stream.bytes_written+10 & 0xFF;
  crc.restart();  

  uint8_t message[10+stream.bytes_written];
  for(int i = 0; i<10; i++){
    message[i]=header[i];
  } 
  for(int i = 0; i<stream.bytes_written; i++){
    message[i+10]= buffer[i];
  }

  //Serial.print("Request: ");
  //for(int i = 0; i<10+stream.bytes_written; i++){
  //  Serial.print(message[i]);
  //}
  Serial.println("");

  WiFiClient client;

  if (!client.connect(host, port)) {
      Serial.println("Connection failed.");
      Serial.println("Waiting 5 seconds before retrying...");
      delay(5000);
      return;
  }
  client.write(message,10+stream.bytes_written);
  readResponse(&client);

  client.stop();

  Serial.println("Waiting 120 seconds before restarting...");
  delay(120000);
}