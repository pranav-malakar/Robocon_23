//Including the necesary libraries
#include <nRF24L01.h>
#include <RF24.h>
#include "CytronMotorDriver.h"
#include <Wire.h>
#include <SPI.h>

RF24 radio(48, 49); // CE, CSN

//BTS Picking Mechanism Pins
#define pickinglpwm 8
#define pickingrpwm 7

//Lead Screw Shooting Mechanism Pins
#define shootinglpwm 5
#define shootingrpwm 6

//L298N Feeding Mechanism Pins
#define feedingPWM 37
#define feedingIN1 39
#define feedingIN2 41

//Relay Module Pins for the Throwing and Picking Mechanism
#define relay1 31
#define relay2 29
#define relay3 27
#define relay4 25
#define relayvcc 23
#define relaygnd 33

#define max_pwm 60

const byte address[6] = "BBBBB"; //Address
uint8_t IN[20]; // Controller Data 
// analog values[0-255] ----> (x_L, y_L, x_R, y_R), (SELECT,L3,R3,START,UP,RIGHT,DOWN,LEFT,L2,R2,L1,R1,TRIANGLE,CIRCLE,CROSS,SQUARE) <---- boolean values[0-1]

//Cytron Motor Driver Pins For the Drive
CytronMD motor1(PWM_DIR, 11, A13);
CytronMD motor2(PWM_DIR, 10, A14);
CytronMD motor3(PWM_DIR, 9, A15);
CytronMD motor4(PWM_DIR, 12, A12);

//Inverse Kinematics code for the Drive 
void convert(int x, int y, int z_rotation)
{

  float WHEEL_GEOMETRY = 0.550 + 0.229; // Hight and width meters
  float WHEEL_RADIUS = 0.0785;          // radius in meters

  x = x-123;
  y = y-132;
  z_rotation = z_rotation-132;
    
  float front_left = (x - y - z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;
  float front_right = (x + y + z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;
  float back_left = (x + y - z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;
  float back_right = (x - y + z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;

  int front_left_ = map(constrain(front_left, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
  int front_right_ = map(constrain(front_right, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
  int back_left_ = map(constrain(back_left, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
  int back_right_ = map(constrain(back_right, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
 
//  char output[100];
//  sprintf(output, "Wheel 1 -> %-4d Wheel 2 -> %-4d Wheel 3 -> %-4d Wheel 4 -> %-4d", front_left_, front_right_, back_left_, back_right_);
//  Serial.println(output);

  //Serial.println(String(front_left)+" "+String(front_right)+" "+String(back_left)+" "+String(back_right));

  motor2.setSpeed(front_left_);  // Motor 1 stops.
  motor3.setSpeed(front_right_); // Motor 2 stops.
  motor4.setSpeed(back_right_);   // Motor 1 stops.
  motor1.setSpeed(back_left_);  // Motor 2 stops.
}

void setup()
{
  delay(2000);
  Serial.begin(9600);
  radio.begin();
  if (radio.isChipConnected()){
    Serial.print("NRF SPI Connected");
  }
  radio.setChannel(100);
  radio.setPayloadSize(20);  
  radio.setDataRate(RF24_2MBPS);
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  
  pinMode(feedingIN1, OUTPUT);
  pinMode(feedingIN2, OUTPUT);
  pinMode(feedingPWM, OUTPUT);
  digitalWrite(feedingPWM, HIGH);
  
  pinMode(pickinglpwm, OUTPUT);
  pinMode(pickingrpwm, OUTPUT);
  
  pinMode(shootinglpwm, OUTPUT);
  pinMode(shootingrpwm, OUTPUT);
  
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  pinMode(relayvcc, OUTPUT);
  pinMode(relaygnd, OUTPUT);
  digitalWrite(relayvcc, HIGH);
  digitalWrite(relaygnd, LOW);
  
//  motor2.setSpeed(0);  // Motor 1 stops.
//  motor3.setSpeed(0); // Motor 2 stops.
//  motor4.setSpeed(0);   // Motor 1 stops.
//  motor1.setSpeed(0); 

}
void loop()
{
  if (radio.available()) {
    radio.read(&IN, sizeof(IN));
    for(int i=0;i<19;i++){
      Serial.print(" ");
      Serial.print(IN[i]);
    }
    Serial.println();// Read the whole data and store it into the IN array
  }
   delay(10);
  
  //Calling Drive Inverse kinematics function 
  convert(IN[1], IN[0], IN[2]); 
  delay(10);

  //Picking Mechanism Right A and B Buttons On the Controller 
  if (IN[12] == 1)
  {
    analogWrite(pickinglpwm, 200);
    analogWrite(pickingrpwm, 0);
    Serial.println("Pickup - going high");
//    delay(100);
  }
  else if (IN[13] == 1) {
    analogWrite(pickinglpwm, 0);
    analogWrite(pickingrpwm, 200);
    Serial.println("Pickup - going low");
//    delay(100);
  }
  else if (IN[12] == 0 && IN[13] == 0)
  {
    analogWrite(pickinglpwm, 0);
    analogWrite(pickingrpwm, 0);
  }

  //Feeding Mechanism Right C Button On the Controller 
  if (IN[8] == 1)
  {
    digitalWrite(feedingIN1, HIGH);
    digitalWrite(feedingIN2, LOW);
    Serial.println("HIT");
  }
  else if (IN[10] == 1)
  {
    digitalWrite(feedingIN1, LOW);
    digitalWrite(feedingIN2, HIGH);
    Serial.println("BACK");
  }
  else if (IN[8] == 0 && IN[10]==0)
  {
    digitalWrite(feedingIN1, LOW);
    digitalWrite(feedingIN2, LOW);
  }

  //Shooting Mechanism Lead Screw Right D and Left A Buttons 
  if (IN[9] == 1)
  {
    analogWrite(shootingrpwm, 0);
    analogWrite(shootinglpwm, 200);
    Serial.println("FORWARD");
  } 
  else if (IN[11] == 1)
  {
    analogWrite(shootinglpwm, 0);
    analogWrite(shootingrpwm, 200);
    Serial.println("BACKWARD");
  }
  else if (IN[9] == 0 && IN[11] == 0)
  {
    analogWrite(shootinglpwm, 0);
    analogWrite(shootingrpwm, 0);
//    Serial.println("STOP");
  }

  //Relays Are HIGH Triggered
  //Relay 1 and 2 Shooting Mechanism Piston Control Left B and C Buttons  
  if (IN[16] == 1)
  {
    Serial.println("Relay2 On");
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, LOW);
  }
  else if (IN[17] == 1)
  {
    Serial.println("Relay1 On");
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, HIGH);
  }
  else if (IN[16] == 0 && IN[17] == 0)
  {
//    Serial.println("No Relay");
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
  }

  //Relay 3 and 4 Picking Mechanism Piston Control Left D and Tog Buttons
  if (IN[18] == 1)
  {
    Serial.println("Relay4 On");
    digitalWrite(relay3, HIGH);
    digitalWrite(relay4, LOW);
  }
  else if (IN[19] == 1)
  {
    Serial.println("Relay3 On");
    digitalWrite(relay3, LOW);
    digitalWrite(relay4, HIGH);
  }
  else if (IN[18]==0 && IN[19]==0)
  {
//    Serial.println("Both Off");
    digitalWrite(relay3, HIGH);
    digitalWrite(relay4, HIGH);
  }
}
