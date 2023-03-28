#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

int i = 0;

RF24 radio(8, 10); // CE, CSN

const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.stopListening();
}

void loop() {
  radio.write(&i, sizeof(i));
  i++;
  Serial.println(i);
  delay(10);
}
