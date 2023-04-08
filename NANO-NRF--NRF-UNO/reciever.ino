#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "DigitalIO.h"

// analog values[0-255] ----> (x_L, y_L, x_R, y_R), (SELECT,L3,R3,START,UP,RIGHT,DOWN,LEFT,L2,R2,L1,R1,TRIANGLE,CIRCLE,CROSS,SQUARE) <---- boolean values[0-1]
uint8_t PS_arr[20];

RF24 radio(8, 10); // CE, CSN

const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  radio.begin();
  if (radio.isChipConnected()) {
    Serial.println("NRF24L01+ CONNECTED TO SPI BUS.");
  }
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    radio.read(&PS_arr, sizeof(PS_arr));
  }
    for (int j=0; j<=19; j++) {    
      Serial.print(PS_arr[j]); d
      Serial.print(", ");
    }
  Serial.println();
  delay(10);
}

//reciever
