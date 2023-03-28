#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


int i;

RF24 radio(8, 10); // CE, CSN

const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    radio.read(&i, sizeof(i));
    Serial.println(i);
  }
  delay(10);
}
