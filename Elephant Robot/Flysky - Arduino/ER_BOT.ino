#include "CytronMotorDriver.h"
#include <IBusBM.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#define lpwm 8   //BTS for pickup
#define rpwm 7   //BTS for pickup
#define lpwms 6  //BTS for leadscrew
#define rpwms 5  //BTS for leadscrew
#define PWM 53   //FEEDING PWM
#define IN1 49   
#define IN2 51
#define relayvcc 23
#define relaygnd 33
#define relay3 27
#define relay4 25
#define relay1 31
#define relay2 29
#define max_pwm1 74
#define max_pwm2 76
#define max_pwm3 72
#define max_pwm4 71
#define pick_max 255
IBusBM ibus;

//object of all motors driven by cytron

CytronMD motor1(PWM_DIR, 11, A14);
CytronMD motor2(PWM_DIR, 10, A13);
CytronMD motor3(PWM_DIR, 9, A12);
CytronMD motor4(PWM_DIR, 12, A15);

//Reading channel value from flysky

int readChannel(byte channelInput, int minLimit, int maxLimit, int defaultValue) {
  uint16_t ch = ibus.readChannel(channelInput);
  if (ch < 100) return defaultValue;
  return map(ch, 1000, 2000, minLimit, maxLimit);
}

// Read switch values from flysky

bool readSwitch(byte channelInput, bool defaultValue) {
  int intDefaultValue = (defaultValue) ? 100 : 0;
  int ch = readChannel(channelInput, 0, 100, intDefaultValue);
  return (ch > 50);
}


//DRIVE CODE TO SET MOTOR SPEED

void convert(int x, int y, int z_rotation) {

  float WHEEL_GEOMETRY = 0.550 + 0.229;  // Hight and width meters
  float WHEEL_RADIUS = 0.0785;           // radius in meters

  float front_left = (x - y - z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;
  float front_right = (x + y + z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;
  float back_left = (x + y - z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;
  float back_right = (x - y + z_rotation * WHEEL_GEOMETRY) / WHEEL_RADIUS;

  int front_left_ = map(constrain(front_left, -1000, 1000), -1000, 1000, -max_pwm2, max_pwm2);
  int front_right_ = map(constrain(front_right, -1000, 1000), -1000, 1000, -max_pwm3, max_pwm3);
  int back_left_ = map(constrain(back_left, -1000, 1000), -1000, 1000, -max_pwm4, max_pwm4);
  int back_right_ = map(constrain(back_right, -1000, 1000), -1000, 1000, -max_pwm1, max_pwm1);

  char output[100];
  // sprintf(output, "Wheel 1 -> %-4d Wheel 2 -> %-4d Wheel 3 -> %-4d Wheel 4 -> %-4d", front_left_, front_right_, back_left_, back_right_);
  // Serial.println(output);
  // Serial.println(String(front_left)+" "+String(front_right)+" "+String(back_left)+" "+String(back_right));
  motor2.setSpeed(front_left_);   // Motor 1 stops.
  motor3.setSpeed(front_right_);  // Motor 2 stops.
  motor4.setSpeed(back_right_);   // Motor 1 stops.
  motor1.setSpeed(back_left_);    // Motor 2 stops.
}




void setup() {
  Serial.begin(9600);
  delay(2000);
  ibus.begin(Serial1);
  digitalWrite(PWM, HIGH);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(PWM, OUTPUT);
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  pinMode(relayvcc, OUTPUT);
  pinMode(relaygnd, OUTPUT);
}
void loop() {
  int X_axis = readChannel(1, -100, 100, 0);
  int Y_axis = readChannel(0, 100, -100, 0);
  int Z_axis = readChannel(3, -100, 100, 0);

  char output_1[100];
  sprintf(output_1, "ch 1 -> %-4d ch 2 -> %-4d ch 3 -> %-4d ", X_axis, Y_axis, Z_axis);
  convert(X_axis, Y_axis, Z_axis);
  delay(10);
  int pickup = readChannel(7, -100, 100, 0);
  int hit = readChannel(8, -100, 100, 0);

  //TO PICKUP THE RINGS

  if (pickup > 0) {
    analogWrite(lpwm, pick_max);
    analogWrite(rpwm, 0);
    delay(100);
  } else if (pickup < 0) {
    analogWrite(rpwm, pick_max);
    analogWrite(lpwm, 0);
    delay(100);
  } else {
    analogWrite(lpwm, 0);
    analogWrite(rpwm, 0);
  }

  //FEEDING

  if (hit > 0) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    delay(800);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    delay(600);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
  }


  int Shoot = readChannel(5, -100, 100, 0);
  int leadscrew = readChannel(6, -100, 100, 0);
  int ch3 = readChannel(9, -100, 100, 0);

  //LEADSCREW

  if (leadscrew > 0) {
    forward();
    Serial.println("FORWARD");
  } else if (leadscrew < 0) {
    backward();
    Serial.println("BACKWARD");
  } else if (leadscrew == 0) {
    stop();
    Serial.println("STOP");
  }

  //RELAY SWITCH TO SHOOT THE RINGS

  if (Shoot > 0) {
    Serial.println("relay2n high");
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, LOW);
  } else if (Shoot < 0) {
    Serial.println("relay1n high");
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, HIGH);
  } else if (Shoot == 0) {
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
  }

  // RELAY SWITCH TO BRING THE SCOOP TOGETHER

  if (ch3 > 0) {
    digitalWrite(relay3, HIGH);
    digitalWrite(relay4, LOW);
  } else if (ch3 < 0) {
    digitalWrite(relay3, LOW);
    digitalWrite(relay4, HIGH);
  } else if (ch3 == 0) {
    digitalWrite(relay3, HIGH);
    digitalWrite(relay4, HIGH);
  }
}

//LEADSCREW BTS FUNCTIONS

void forward() {
  analogWrite(rpwms, 0);
  analogWrite(lpwms, 200);
}
void backward() {
  analogWrite(lpwms, 0);
  analogWrite(rpwms, 200);
}
void stop() {
  analogWrite(lpwms, 0);
  analogWrite(rpwms, 0);
}