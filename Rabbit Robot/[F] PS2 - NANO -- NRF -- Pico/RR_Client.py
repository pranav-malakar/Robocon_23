#RR_Server
#Importing necessary header files
from machine import Pin, UART, PWM, SPI
from time import sleep
import ustruct as struct
from nrf24l01 import *
from micropython import const

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

'''
Rabbit Robot

M - Motor
LA - Linear Actuator
S - Servo
P - Piston
PM - Picking Motor
FM - FLipping Motor

                             __________________
                             ||______________||
                            //                \\       
                          // ||              || \\
                        //   ||LA1        LA2||   \\          
                     S1 |____||______________||____| S2                          
                   PM1 ||                          || PM2
                        |__________________________|
                        |                  ||| FM  |
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

#Defining pins for picking and flipping motors, linear actuator, servo
relay = Pin(8,Pin.OUT)

pick_mp1 = Pin(5,Pin.OUT)
pick_mp2 = Pin(6,Pin.OUT)
pick_men = PWM(Pin(7,Pin.OUT))

la_mp1 = Pin(4,Pin.OUT)
la_mp2 = Pin(3,Pin.OUT)
la_men = PWM(Pin(2,Pin.OUT))

la_state = 0

servo1 = PWM(Pin(14,Pin.OUT))
servo2 = PWM(Pin(15,Pin.OUT))

flip_mp1 = Pin(10,Pin.OUT)
flip_mp2 = Pin(11,Pin.OUT)
flip_en = PWM(Pin(12,Pin.OUT))


#Funtion for reading data from NRF and sending to PICO2
no_of_channels=20
JS_values = [0]*no_of_channels

def readval():
    global JS_values
    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            JS_values = list(struct.unpack("20B",buf))
            JS_values[0] -= 132
            JS_values[1] -= 123
            JS_values[2] -= 123
            JS_values[3] -= 123
            #print(JS_values)
        
    message=','.join(map(str,JS_values[2:4]+JS_values[14:16]))
    uart.write(message.encode('utf-8'))    
    
#This function is used for the movement of motor which is responsible for picking
def pickmove(dir):
    
    if not dir:
        print("Picking moving upwards")
    else:
        print("Picking moving downwards")

    pick_mp1.value(not dir)
    pick_mp2.value(dir)
    pick_men.duty_u16(6500)

#This function is used for stopping the movement of motor which is responsible for picking
def pickstop():
    
    pick_mp1.value(1)
    pick_mp2.value(1)
    pick_men.duty_u16(0)
    
    #print("Picking stop")
    
#This function is used more movement of linear actuator
def lamotion():

    global la_state
    
    if la_state==0:
        la_mp1.value(1)
        la_mp2.value(0)
        la_state=1
        print("Linear Actuator Extend")
    else:
        la_mp1.value(0)
        la_mp2.value(1)
        la_state=0
        print("Linear Actuator Retract")
        
#Main program starts
la_men.duty_u16(65032)

while True:
    
    readval()
    if JS_values[1]>75: #Left Joystick Y axis is used for picking
        pickmove(dir=1)
    elif JS_values[1]<-75:
        pickmove(dir=0)
    else:
        pickstop()
    
    if JS_values[18]: #X is used for controlling motion of linear actuator
        while True:
            readval()
            if not JS_values[18]:
                break
        lamotion() 
    
    if JS_values[16]>0: #Triangle is used for controlling relay
        print("Relay on")
        relay.value(1)
    else:
        #print("Relay off")
        relay.value(0)
    
    sleep(0.01)
