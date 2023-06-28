#include <PS2X_lib.h>  //for v1.6
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//ps2 pinouts
#define PS2_CLK        13  
#define PS2_DAT        12      
#define PS2_CMD        11   
#define PS2_SEL        4    


// analog values[0-255] ----> (x_L, y_L, x_R, y_R), (SELECT,L3,R3,START,UP,RIGHT,DOWN,LEFT,L2,R2,L1,R1,TRIANGLE,CIRCLE,CROSS,SQUARE) <---- boolean values[0-1]

uint8_t PS_arr[20]; //unsigned 8-bit int range (0-255)
PS2X ps2x; // create PS2 Controller Class
int error = 0;


RF24 radio(A0, 5); //CE, CSN //(A0, 5) for second dsb
const byte address[6] = "DIVYA"; // "BBBBB" on ER, "AAAAA" on RR


void setup() {
  Serial.begin(9600);
  
  //last two args are for pressure and rumble
  error = ps2x.config_gamepad(PS2_CLK, PS2_CMD, PS2_SEL, PS2_DAT, false, false);
  if(error == 0){
    Serial.println("Found Controller, configured successful ");
  }  
  else if(error == 1)
    Serial.println("No controller found, check wiring, see readme.txt to enable debug. visit www.billporter.info for troubleshooting tips");
   
  else if(error == 2)
    Serial.println("Controller found but not accepting commands. see readme.txt to enable debug. Visit www.billporter.info for troubleshooting tips");

  else if(error == 3)
    Serial.println("Controller refusing to enter Pressures mode, may not support it. ");

  //set joystick arrays as all zeroes.
  memset(&PS_arr, 0, sizeof(PS_arr));
  
  radio.begin();
  if (radio.isChipConnected()) {
    Serial.println("nrf24l01+ connected through SPI.");
  }
  else {
    Serial.println("nrf24l01+ NOT connected through SPI.");
  }
  radio.setChannel(100); //communication channel
  radio.setPayloadSize(20); //number of bytes to be sent. Maximum is 32 bytes at once.
  radio.setDataRate(RF24_2MBPS); //2 MBPS data rate, options: (RF24_250KBPS,RF24_1MBPS,RF24_2MBPS)
  radio.openWritingPipe(address); //set the writing (pipe) address
  radio.stopListening(); //Set module as transmitter
}


void loop() {
  //read controller
  ps2x.read_gamepad(false, 0x0); //args are pressure, rumble

  //analog JS readings
  PS_arr[0] = ps2x.Analog(PSS_LX);  
  PS_arr[1] = ps2x.Analog(PSS_LY);
  PS_arr[2] = ps2x.Analog(PSS_RX);
  PS_arr[3] = ps2x.Analog(PSS_RY);


  //digital Button readings
    for (unsigned long i=0x1,p=4; i<=0x8000; i=i*2,p++) {
      PS_arr[p] = ps2x.Button(i);
    }

  //print array IF empty packet received as acknowledgement payload from receiver to transmitter (data sent successfully).
  if (radio.write(&PS_arr, sizeof(PS_arr))) {
   for (int j=0; j<=19; j++) {
    Serial.print(PS_arr[j]);
    Serial.print(" ");
  }
  Serial.println();
  }

  
  // radio.write(&PS_arr, sizeof(PS_arr));
  //  for (int j=0; j<=19; j++) {
  //   Serial.print(PS_arr[j]);
  //   Serial.print(" ");
  //  }
  //   Serial.println();


}
