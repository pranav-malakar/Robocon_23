//ER_Main
//Importing necessary header files
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h>
#include <SPI.h>

//Initializing NRF and address
RF24 radio(48, 49);               // CE, CSN
const byte address[6] = "DIVYA";  //Address for communication between NRF
int8_t command[20];
//analog values[0-255] ----> (x_L, y_L, x_R, y_R), (SELECT,L3,R3,START,UP,RIGHT,DOWN,LEFT,L2,R2,L1,R1,TRIANGLE,CIRCLE,CROSS,SQUARE) <---- boolean values[0-1]
//index value-                 0    1    2    3       4    5  6    7   8    9    10   11  12 13 14 15    16      17     18    19

/*

  Elephant Robot


  M - Motor
  P - Piston
  PM - Picking Motor
  FM - Feeding Motor
  SM - Shooting Motor

                    P2  | -->                  <-- | P3
                        ||||                    ||||
                        |                          |
                   PM1 ||                          || PM2
                        |__________|| FM
                   M4 |||                          ||| M3
                      |||        --> ||            |||
                        |     |||| \_||_/          |
                        |      P1    ||            |
                        |            ||            |
                        |            ||            |
                        |            ||            |
                        |            ||            |
                   M1 |||            ||||          ||| M2
                      |||              SM          |||
                        |__________|


*/

//Defining pins for sensors
#define laser 42
#define ldr 46

//Defining pins for Drive (Cytron)
#define drive_m1dir A14
#define drive_m1pwm 9
#define drive_m2dir A13
#define drive_m2pwm 12
#define drive_m3dir A12
#define drive_m3pwm 11
#define drive_m4dir A15
#define drive_m4pwm 10

//Defining pins for motors for picking (Cytron)
#define pick_m1dir 7
#define pick_m1pwm 5
#define pick_m2dir 8
#define pick_m2pwm 6

//Defining pins for motor for shooting (Cytron)
#define shoot_mdir 22
#define shoot_mpwm 3

//Defining pins for motor for feeding (L298N)
#define feed_min1 32
#define feed_min2 34
#define feed_mpwm 44

//Defining pins for relay
#define relay_pick1 37
#define relay_pick2 35
#define relay_shoot1 33
#define relay_shoot2 31

//This function is used for moving the bot
void botmove(int Vx = 0, int Vy = 0) {
  Vx = Vx + 5;
  Vy = Vy + 5;
  int m1speed = 70 * ((float)(Vx - Vy) / 128);
  int m2speed = 70 * ((float)(Vx + Vy) / 128);
  int m3speed = 70 * ((float)(-Vx + Vy) / 128);
  int m4speed = 70 * ((float)(-Vx - Vy) / 128);

  digitalWrite(drive_m1dir, m1speed > 0);
  digitalWrite(drive_m2dir, m2speed > 0);
  digitalWrite(drive_m3dir, m3speed > 0);
  digitalWrite(drive_m4dir, m4speed > 0);

  analogWrite(drive_m1pwm, abs(m1speed));
  analogWrite(drive_m2pwm, abs(m2speed));
  analogWrite(drive_m3pwm, abs(m3speed));
  analogWrite(drive_m4pwm, abs(m4speed));

  Serial.println(String(m1speed) + " " + String(m2speed) + " " + String(m3speed) + " " + String(m4speed));
}

//This function is used for rotating the bot
void botrotate(int dir = 0, int speed = 0) {
  if (dir == 0)
    Serial.println("Bot Rotate Anti-Clockwise");
  else
    Serial.println("Bot Rotate Clockwise");

  digitalWrite(drive_m1dir, dir);
  digitalWrite(drive_m2dir, dir);
  digitalWrite(drive_m3dir, dir);
  digitalWrite(drive_m4dir, dir);

  analogWrite(drive_m1pwm, speed);
  analogWrite(drive_m2pwm, speed);
  analogWrite(drive_m3pwm, speed);
  analogWrite(drive_m4pwm, speed);
}

//This function is used for stopping the bot
void botstop() {
  digitalWrite(drive_m1dir, 0);
  digitalWrite(drive_m2dir, 0);
  digitalWrite(drive_m3dir, 0);
  digitalWrite(drive_m4dir, 0);

  analogWrite(drive_m1pwm, 0);
  analogWrite(drive_m2pwm, 0);
  analogWrite(drive_m3pwm, 0);
  analogWrite(drive_m4pwm, 0);

  Serial.println("Bot Stop");
}

//This function is used for the movement of motor which is responsible for picking
void pickmove(int dir = 0, int speed = 0) {
  if (dir == 0)
    Serial.println("Picking moving upwards");
  else
    Serial.println("Picking moving downwards");

  digitalWrite(pick_m1dir, dir);
  digitalWrite(pick_m2dir, dir);

  analogWrite(pick_m1pwm, speed);
  analogWrite(pick_m2pwm, 124);
}

//This function is used for stopping the movement of motor which is responsible for picking
void pickstop() {
  digitalWrite(pick_m1dir, 0);
  digitalWrite(pick_m2dir, 0);

  analogWrite(pick_m1pwm, 0);
  analogWrite(pick_m2pwm, 0);

  //Serial.println("Picking Stop");
}

//This function is used for the movement of motor which is responsible for shooting
void shootmove(int dir = 0, int speed = 0) {

  if (dir == 0)
    Serial.println("Shooting moving upwards");
  else
    Serial.println("Shooting moving downwards");

  digitalWrite(shoot_mdir, !dir);
  analogWrite(shoot_mpwm, speed);
}

//This function is used for stopping the movement of motor which is responsible for shooting
void shootstop() {
  digitalWrite(shoot_mdir, 0);
  analogWrite(shoot_mpwm, 0);
  //Serial.println("Shooting Stop");
}

//function for feeding rings to the bot
void feedin() {
  Serial.println("Feed rod Back");
  digitalWrite(feed_min1, LOW);
  digitalWrite(feed_min2, HIGH);
  analogWrite(feed_mpwm, 150);
}

void feedout() {
  Serial.println("Feed");
  digitalWrite(feed_min1, HIGH);
  digitalWrite(feed_min2, LOW);
  analogWrite(feed_mpwm, 150);
}

void feeds() {
  digitalWrite(feed_min1, HIGH);
  digitalWrite(feed_min2, HIGH);
  analogWrite(feed_mpwm, 0);
}

//Beginning serial monitor and radio communication and respective initialising pins
void setup() {
  Serial.begin(9600);
  radio.begin();

  //Initialising NRF
  if (radio.isChipConnected()) {
    Serial.print("NRF SPI is Connected");
  }
  radio.setChannel(100);
  radio.setPayloadSize(20);
  radio.setDataRate(RF24_2MBPS);
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();

  //Setting pin mode for motors for drive
  pinMode(drive_m1dir, OUTPUT);
  pinMode(drive_m1pwm, OUTPUT);
  pinMode(drive_m2dir, OUTPUT);
  pinMode(drive_m2pwm, OUTPUT);
  pinMode(drive_m3dir, OUTPUT);
  pinMode(drive_m3pwm, OUTPUT);
  pinMode(drive_m4dir, OUTPUT);
  pinMode(drive_m4pwm, OUTPUT);

  //Setting pin mode for motors for picking
  pinMode(pick_m1dir, OUTPUT);
  pinMode(pick_m1pwm, OUTPUT);
  pinMode(pick_m2dir, OUTPUT);
  pinMode(pick_m2pwm, OUTPUT);

  //Setting pin mode for motors for shooting
  pinMode(shoot_mdir, OUTPUT);
  pinMode(shoot_mpwm, OUTPUT);

  //Setting pin mode for motors for feeding
  pinMode(feed_min1, OUTPUT);
  pinMode(feed_min2, OUTPUT);
  pinMode(feed_mpwm, OUTPUT);

  //Setting pin mode for relay
  pinMode(relay_pick1, OUTPUT);
  pinMode(relay_pick2, OUTPUT);
  pinMode(relay_shoot1, OUTPUT);
  pinMode(relay_shoot2, OUTPUT);

  //Setting pin mode for sensors
  pinMode(ldr, INPUT);
  pinMode(laser, OUTPUT);
}

//Main program starts
void loop() {
  //Reading data from NRF
  if (radio.available()) {
    radio.read(&command, sizeof(command));
    command[1] = command[1] - 128;
    command[2] = (int)command[2] - 128;
    command[3] = (int)command[3] - 128;
    //            for(int i = 0; i < 20; i++)
    //            {
    //                Serial.print(command[i]);
    //                Serial.print(" ");
    //            }
    //            Serial.println();
  }


  //Drive Control
  if (command[2] > -5 || command[2] < -5 || command[3] > -5 || command[3] < -5) //Right Joystick is used for controlling the motion of the drive
  {
    botmove(command[2], command[3]); //Vx,Vy
  }  else if (command[14])              //L1 is used for rotating the bot anti-clockwise
  {
    botrotate(1, 40);      //dir,speed
  }  else if (command[15])  //R1 is used for rotating the bot clockwise
  {
    botrotate(0, 40);  //dir,speed
  } else {
    botstop();
  }
  //  //Picking Control
  if (command[10])  //L2 is used for picking down
  {
    pickmove(0, 120);      //dir,speed
  } else if (command[8])  //R2 is used for picking up
  {
    digitalWrite(laser, HIGH);
    bool laservalue = digitalRead(ldr);
    if (laservalue == 0)  //If the LDR is giving a low signal then the picking can move upward
      pickmove(1, 120);   //dir,speed

    else
    {
      pickstop();
    }
  }
  else {
    digitalWrite(laser, LOW);
    pickstop();
  }

  // Feeding Control
  if (command[9] == 1)
  {
    feedout();
  }
  else if (command[11] == 1)
  {
    feedin();
  }
  else if (command[9] == 0 && command[11] == 0)
  {
    feeds();
  }

  //Shooting Control
  if (command[1] < -80) //Left Joystick Y axis is used for controlling the movement of motor for shooting
  {

    shootmove(0, 255);
  }
  else if (command[1] > 80) {

    shootmove(1, 255);
  }
  else {
    shootstop();
  }

  // Relay Control
  // Shooting
  if (command[17] == 1)
  {
    digitalWrite(relay_shoot1, LOW);
    digitalWrite(relay_shoot2, HIGH);
  }
  else if (command[19] == 1)
  {
    digitalWrite(relay_shoot1, HIGH);
    digitalWrite(relay_shoot2, LOW);
  }
  else if (command[17] == 0 && command[19] == 0)
  {
    digitalWrite(relay_shoot1, HIGH);
    digitalWrite(relay_shoot2, HIGH);
  }
  delay(10);
}
