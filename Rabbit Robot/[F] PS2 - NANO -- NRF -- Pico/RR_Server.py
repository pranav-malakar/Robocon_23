#RR_Server
#Importing necessary header files
from machine import Pin, UART, PWM, SPI, I2C
from time import sleep
import ustruct as struct
from nrf24l01 import *
from micropython import const
from pca9685 import PCA9685

#Setting channel, baud rate and pins for communication between Pico to Pico
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

#Setting up SPI pins for NRF
pipe = (b"\x41\x41\x41\x41\x41") # 'AAAAA' on the ardinuo
spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cfg = {"spi": 0, "miso": 16, "mosi": 19, "sck": 18, "csn": 17, "ce": 20} 
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)

#Initializing NRF
nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, channel = 100, payload_size=20)
nrf.open_rx_pipe(0, pipe)
nrf.set_power_speed(POWER_1, SPEED_2M) # power1 = -12 dBm, speed_2m = 2 mbps
nrf.start_listening()
print('readSensorLoop, waiting for packets... (ctrl-C to stop)')

#Setting up I2c pins for PCA9685
SDA = Pin(6)
SCL = Pin(7)
#i2c = I2C(id=1, sda=SDA, scl=SCL,freq=400000)

#Initializing PCA9685
PCA1_ADDR = 0x41 
i2c = I2C(id=1, sda=SDA, scl=SCL, freq=400000) 
print("device found at address:", hex(i2c.scan()[0]))
pca=PCA9685(i2c=i2c,address=0x41)
pca.freq(100)

'''
Rabbit Robot

M - Motor
LA - Linear Actuator
S - Servo
P - Piston
PM - Picking Motor


                             __________________
                             ||______________||
                            //                \\       
                          //                    \\
                        //                        \\          
                     S1 |__________________________| S2                          
                   PM1 ||                          || PM2
                     S3 |__________________________| S4
                        |                          |
                        |      \            /      |
                        |        \        /        |
                        |          \    /          |
                        |            ||            |
                   M2 |||            ||            ||| M1
                      |||            || P          |||
                        |__________________________|
                                    ----
                                    ----
                                     M3
                                     
        
'''

#Defining pins for relay and L298N on PCA9685
pick_mp1 = 3
pick_mp2 = 4
pick_men = 5

relay = 12

#Defining pins for servo, laser, ldr
servo_feed1 = PWM(Pin(2,Pin.OUT))
servo_feed1.freq(50)
servo_feed2 = PWM(Pin(3,Pin.OUT))
servo_feed2.freq(50)
servo_flip1 = PWM(Pin(4,Pin.OUT))
servo_flip1.freq(50)
servo_flip2 = PWM(Pin(5,Pin.OUT))
servo_flip2.freq(50)

servo_feed_state=1
servo_flip_state=1

laser = Pin(27,Pin.OUT)
ldr = Pin(26,Pin.IN)

#Funtion for reading data from NRF and sending to PICO2
no_of_channels = 20
JS_values = [0]*no_of_channels

def readval():
    global JS_values
    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            JS_values = list(struct.unpack("20B",buf))
            JS_values[0] -= 128
            JS_values[1] -= 128
            JS_values[2] -= 128
            JS_values[3] -= 128
            #JS_values[:4] = [x*-1 for x in JS_values[:4]]
            #print(JS_values)
        
    message=','.join(map(str,JS_values[2:4]+JS_values[14:16]))
    uart.write(message.encode('utf-8'))   
    
#This function is used for the movement of motor which is responsible for picking
def pickmove(dir):
    
    if not dir:
        print("Picking moving upwards")
    else:
        print("Picking moving downwards")
    
    pca.pwm(pick_mp1,0,(dir)*4095)
    pca.pwm(pick_mp2,0,(not dir)*4095)
    pca.pwm(pick_men,0,4095)
    
#This function is used for stopping the movement of motor which is responsible for picking
def pickstop():
    
    #Motors have low torque
    pca.pwm(pick_mp1,0,0)
    pca.pwm(pick_mp2,0,4095)
    pca.pwm(pick_men,0,400)
    
    #print("Picking stop")
        
def servofeed():
    
    global servo_feed_state
    
    #2500 = 0 degree, 7500 = 180 degree
    if servo_feed_state==0:
        servo_feed1.duty_u16(4000)
        servo_feed2.duty_u16(5500)
        servo_feed_state=1
        print("Servo Scoop Out")
    else:
        servo_feed1.duty_u16(6000)
        servo_feed2.duty_u16(3500)
        servo_feed_state=0
        print("Servo Scoop In")

def servoflip():
    
    global servo_flip_state
    
    #2500 = 0 degree, 7500 = 180 degree
    if servo_flip_state==0:
        servo_flip1.duty_u16(3500)
        servo_flip2.duty_u16(6500)
        servo_flip_state=1
        print("Servo Flip Up")
    else:
        servo_flip1.duty_u16(6000)
        servo_flip2.duty_u16(3500)
        servo_flip_state=0
        print("Servo Flip Down")
    
#Main program starts and setting servos to their initial positions
servo_feed1.duty_u16(3000)
servo_feed2.duty_u16(6500)
servo_flip1.duty_u16(3500)
servo_flip2.duty_u16(6500)
while True:
    
    readval()
    if JS_values[12]: #L2 is used for picking up
        laser.value(0)
        pickmove(dir=1)
    elif JS_values[13]: #R2 is used for picking up
        laser.value(1)
        if not ldr.value():
            pickmove(dir=0)
        else:
            pickstop()
        
    else:
        laser.value(0)
        pickstop()
    
    if JS_values[19]: #Square is used for controlling motion of linear actuator
        while True:
            readval()
            if not JS_values[19]:
                break
        servofeed()
    
    if JS_values[17]: #Circle is used for controlling motion of linear actuator
        while True:
            readval()
            if not JS_values[17]:
                break
        servoflip() 
    
    if JS_values[16]>0: #Triangle is used for controlling relay
        print("Relay on")
        pca.pwm(relay,0,4095)
    else:
        #print("Relay off")
        pca.pwm(relay,0,0)
        
    if JS_values[18]: #X for automation
        while True:
            readval()
            if not JS_values[18]:
                break
        servofeed()
        sleep(0.5)
        servofeed()
        sleep(0.5)
        servoflip()
        sleep(0.5)
        servoflip()
        
    sleep(0.01)
