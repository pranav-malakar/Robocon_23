#include <nRF24L01.h>
#include <RF24.h>

#define laser A2
#define sensor A1
// Including the necesary libraries

#include "CytronMotorDriver.h"
#include <Wire.h>
#include <SPI.h>

RF24 radio(48, 49); // CE, CSN

// BTS Picking Mechanism Pins
#define pickinglpwm 6
#define pickingrpwm 5

// Lead Screw Shooting Mechanism Pins
#define shootinglpwm 8
#define shootingrpwm 7

// L298N Feeding Mechanism Pins
#define feedingPWM 30
#define feedingIN1 32
#define feedingIN2 34

// Relay Module Pins for the Throwing and Picking Mechanism
#define relay1 31
#define relay2 29
#define relay3 27
#define relay4 25

#define max_pwm 60

const byte address[6] = "BBBBB"; // Address
uint8_t IN[20];                  // Controller Data
// analog values[0-255] ----> (x_L, y_L, x_R, y_R), (SELECT,L3,R3,START,UP,RIGHT,DOWN,LEFT,L2,R2,L1,R1,TRIANGLE,CIRCLE,CROSS,SQUARE) <---- boolean values[0-1]

// Cytron Motor Driver Pins For the Drive
CytronMD motor1(PWM_DIR, 12, A13);
CytronMD motor2(PWM_DIR, 11, A12);
CytronMD motor3(PWM_DIR, 10, A15);
CytronMD motor4(PWM_DIR, 9, A14);

// Inverse Kinematics code for the Drive
void convert(int x, int y)
{

  // float WHEEL_GEOMETRY = 0.550 + 0.229; // Hight and width meters
  float WHEEL_RADIUS = 0.0785; // radius in meters

  x = 128 - x;
  y = y - 128;

  float front_left = (x - y) / WHEEL_RADIUS;
  float front_right = (x + y) / WHEEL_RADIUS;
  float back_left = (x + y) / WHEEL_RADIUS;
  float back_right = (x - y) / WHEEL_RADIUS;

  int front_left_ = map(constrain(front_left, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
  int front_right_ = map(constrain(front_right, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
  int back_left_ = map(constrain(back_left, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);
  int back_right_ = map(constrain(back_right, -1000, 1000), -1000, 1000, -max_pwm, max_pwm);

  char output[100];
  sprintf(output, "Wheel 1 -> %-4d Wheel 2 -> %-4d Wheel 3 -> %-4d Wheel 4 -> %-4d", front_left_, front_right_, back_left_, back_right_);
  //Serial.println(output);

  //Serial.println(String(front_left) + " " + String(front_right) + " " + String(back_left) + " " + String(back_right));

  motor2.setSpeed(front_left_);  // Motor 1 stops.
  motor3.setSpeed(front_right_); // Motor 2 stops.
  motor4.setSpeed(back_right_);  // Motor 1 stops.
  motor1.setSpeed(back_left_);   // Motor 2 stops.
}

void setup()
{
  Serial.begin(9600);
  pinMode(laser, OUTPUT);
  pinMode(sensor, INPUT);
  radio.begin();
  if (radio.isChipConnected())
  {
    Serial.print("NRP SPI Connected");
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
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);
  motor1.setSpeed(0);
  memset(IN, 0, sizeof(IN));
}
void loop()
{
 
  if (radio.available())
  {
    radio.read(&IN, sizeof(IN));
    for (int i = 0; i < 19; i++)
    {
      Serial.print(" ");
      Serial.print(IN[i]);
    }
    Serial.println(); // Read the whole data and store it into the IN array
  }
  // delay(10);
  // Calling Drive Inverse kinematics function
  convert(IN[3], IN[2]);
  //, IN[0] 3RD ARG FOR ROTATION
  if (IN[14])
  {
    motor1.setSpeed(-max_pwm);
    motor2.setSpeed(-max_pwm);
    motor3.setSpeed(max_pwm);
    motor4.setSpeed(max_pwm);
  }
  else if (IN[15])
  {
    motor1.setSpeed(max_pwm);
    motor2.setSpeed(max_pwm);
    motor3.setSpeed(-max_pwm);
    motor4.setSpeed(-max_pwm);
  }

  // delay(10);
  // Picking Mechanism Right A and B Buttons On the Controller
  if (IN[12] == 1)
  {
    digitalWrite(laser, HIGH);
    bool laservalue = digitalRead(sensor);
    if(laservalue == 0)
    {
      analogWrite(pickinglpwm, 200);
      analogWrite(pickingrpwm, 0);
      Serial.println("Pickup - going high");
    }
    else
    {
    analogWrite(pickinglpwm, 0);
    analogWrite(pickingrpwm, 0);
    }
  }
  else if (IN[13] == 1)
  {
    analogWrite(pickinglpwm, 0);
    analogWrite(pickingrpwm, 200);
    Serial.println("Pickup - going low");
    // delay(100);
  }
  else if (IN[12] == 0 && IN[13] == 0)
  {
    analogWrite(pickinglpwm, 0);
    analogWrite(pickingrpwm, 0);
    digitalWrite(laser, LOW);
  }
  // Feeding Mechanism Right C Button On the Controller
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
  else if (IN[8] == 0 && IN[10] == 0)
  {
    digitalWrite(feedingIN1, LOW);
    digitalWrite(feedingIN2, LOW);
  }
  // Shooting Mechanism Lead Screw Right D and Left A Buttons
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
  else if ((IN[9] == 0 && IN[11] == 0))
  {
    analogWrite(shootinglpwm, 0);
    analogWrite(shootingrpwm, 0);
    // Serial.println("STOP");
  }

  // Relays Are HIGH Triggered
  // Relay 1 and 2 Shooting Mechanism Piston Control Left B and C Buttons
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
    // Serial.println("No Relay");
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
  }

  // Relay 3 and 4 Picking Mechanism Piston Control Left D and Tog Buttons
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
  else if (IN[18] == 0 && IN[19] == 0)
  {
    // Serial.println("Both Off");
    digitalWrite(relay3, HIGH);
    digitalWrite(relay4, HIGH);
  }
}

/* WHAT'S THERE ON EACH INDEX:
0 = left x
1 = left y
2 = right x
3 = right y
4 = SELECT
5 = L3
6 = R3
7 = START
8 = UP
9 = RIGHT
10 = DOWN
11 = LEFT
12 = L2
13 = R2
14 = L1
15 = R1
16 = TRIANGLE
17 = CIRCLE
18 = CROSS
19 = SQUARE
*/
