#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(A0, 10); // CE, CSN

const byte address[6] = "00001";

uint16_t IN[13];

void setup() {
  Serial.begin(9600);
  
  radio.begin();
  radio.setChannel(100);
  radio.setPayloadSize(26);
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

void loop() {
  // Check whether there is data to be received
  if (radio.available()) {
    radio.read(&IN, sizeof(IN)); // Read the whole data and store it into the 'data' structure
  }
  for(int i=0;i<13;i++){
    Serial.print(" ");
    Serial.print(IN[i]);
  }
  Serial.println();
}
