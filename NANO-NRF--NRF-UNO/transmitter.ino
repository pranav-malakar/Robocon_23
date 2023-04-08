#include <PS2X_lib.h>  //for v1.6
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define PS2_DAT        12  //14    
#define PS2_CMD        11  //15 
#define PS2_SEL        4  //16 
#define PS2_CLK        13  //17 

// analog values[0-255] ----> (x_L, y_L, x_R, y_R), (SELECT,L3,R3,START,UP,RIGHT,DOWN,LEFT,L2,R2,L1,R1,TRIANGLE,CIRCLE,CROSS,SQUARE) <---- boolean values[0-1]
uint8_t PS_arr[20];

PS2X ps2x; // create PS2 Controller Class

RF24 radio(A0, 10); // CE, CSN

int error = 0;
byte type = 0;

const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  
  error = ps2x.config_gamepad(PS2_CLK, PS2_CMD, PS2_SEL, PS2_DAT, false, false);
  if(error == 0){
    Serial.print("Found Controller, configured successful ");
  }  
  else if(error == 1)
    Serial.println("No controller found, check wiring, see readme.txt to enable debug. visit www.billporter.info for troubleshooting tips");
   
  else if(error == 2)
    Serial.println("Controller found but not accepting commands. see readme.txt to enable debug. Visit www.billporter.info for troubleshooting tips");

  else if(error == 3)
    Serial.println("Controller refusing to enter Pressures mode, may not support it. ");
  
//  Serial.print(ps2x.Analog(1), HEX);
  
  type = ps2x.readType(); 
  switch(type) {
    case 0:
      Serial.print("Unknown Controller type found ");
      break;
    case 1:
      Serial.print("DualShock Controller found ");
      break;
    case 2:
      Serial.print("GuitarHero Controller found ");
      break;
	case 3:
      Serial.print("Wireless Sony DualShock Controller found ");
      break;
   }

  memset(&PS_arr, 0, sizeof(PS_arr));
  
  radio.begin();
  if (radio.isChipConnected()) {
    Serial.println("nrf24l01+ connected through SPI.");
  }
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.stopListening();
}

void loop() {
  if (error)  {
    return;
  }
  else{
  ps2x.read_gamepad(false, 0x0); //read controller
  //analog JS readings
  PS_arr[0] = ps2x.Analog(PSS_LX);	
	PS_arr[1] = ps2x.Analog(PSS_LY);
  PS_arr[2] = ps2x.Analog(PSS_RX);
  PS_arr[3] = ps2x.Analog(PSS_RY);
  //digital Button readings
  if (ps2x.NewButtonState()) {
    for (unsigned long i=0x1,p=4; i<=0x8000; i=i*2,p++) {
      PS_arr[p] = ps2x.Button(i); 
    }
  }
  
    radio.write(&PS_arr, sizeof(PS_arr));

  for (int j=0; j<=19; j++) {
    Serial.print(PS_arr[j]);
    Serial.print(", ");
  }
  Serial.println();

  // if(PS_arr[4])         //will be TRUE as long as button is pressed
  //     Serial.println("Select is being held");
  //   if(PS_arr[5])
  //     Serial.println("L3 is being held");      
  //   if(PS_arr[6])
  //     Serial.println("R3 pressed");
  //   if(PS_arr[7])
  //     Serial.println("START pressed");
  //   if(PS_arr[8])
  //       Serial.println("UP pressed");
  //   if(PS_arr[9])
  //     Serial.println("RIGHT pressed");         
  //   if(PS_arr[10])
  //     Serial.println("DOWN pressed");
  //   if(PS_arr[11])
  //     Serial.println("LEFT pressed");
  //   if(PS_arr[12])
  //     Serial.println("L2 pressed");
  //   if(PS_arr[13])
  //     Serial.println("R2 pressed");       
  //   if(PS_arr[16])         
  //     Serial.println("Triangle pressed");
  //   if(PS_arr[17])         
  //     Serial.println("Circle pressed");  
  //   if(PS_arr[18])         
  //     Serial.println("Cross pressed");
  //   if(PS_arr[19])         
  //     Serial.println("Square pressed");

  //   if(PS_arr[14] || PS_arr[15]) { //print stick values if either is TRUE
  //     Serial.print("Stick Values:");
  //     Serial.print(PS_arr[0]); //Left stick, Y axis. Other options: LX, RY, RX  
  //     Serial.print(",");
  //     Serial.print(PS_arr[1]); 
  //     Serial.print(",");
  //     Serial.print(PS_arr[2]); 
  //     Serial.print(",");
  //     Serial.println(PS_arr[3]); 
  //   }   
  
  //memset(&PS_arr, 0, sizeof(PS_arr));
  delay(50);
  }
}
