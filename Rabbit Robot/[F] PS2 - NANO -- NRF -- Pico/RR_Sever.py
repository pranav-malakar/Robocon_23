#RR_Server
#Importing necessary header files
from machine import Pin, UART, PWM
from time import sleep
import ustruct as struct
from nrf24l01 import *
from micropython import const

#Setting channel, baud rate and pins for communication between Pico to Pico
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

#Setting up SPI pins for NRF
pipe = (b"\x41\x41\x41\x41\x41") # 'AAAAA' on the ardinuo
cfg = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 14, "ce": 17}   
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
'''
#Defining pins for picking and flipping motors, linear actuator, servo
relay = Pin(8,Pin.OUT)

pick_mp1 = Pin(5,Pin.OUT)
pick_mp2 = Pin(6,Pin.OUT)
pick_men = PWM(Pin(7))

la_mp1 = Pin(4,Pin.OUT)
la_mp2 = Pin(3,Pin.OUT)
la_men = PWM(Pin(2))

#la_state = 0

'''
'''
servo1 = PWM(Pin())
servo2 = PWM(Pin())

flip_mp1 = Pin(10,Pin.OUT)
flip_mp2 = Pin(11,Pin.OUT)
flip_en = PWM(Pin(12))
'''

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
    print(JS_values)
    message=','.join(map(str,JS_values[0:4]+JS_values[14:16]))
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
    
    print("Picking stop")
    
#This function is used more movement of linear actuator
def lamotion(val):

    if val>30:
        la_mp1.value(1)
        la_mp2.value(0)
        print("Linear Actuator Extend")
    elif val<-30:
        la_mp1.value(0)
        la_mp2.value(1)
        print("Linear Actuator Retract")
    else:
        la_mp1.value(0)
        la_mp2.value(0)
        
#Main program starts
la_men.duty_u16(65032)
while True:
    
    readval()
    '''
    if command[2]>80: #command[2] is used for picking
        pickmove(dir=0)
    elif command[2]<-80:
        pickmove(dir=1)
    else:
        pickstop()
    
    lamotion(command[4]) #command[4] is used for controlling motion of linear actuator
    
    if command[5]>0: #command[5] is used for controlling relay
        print("Relay on")
        relay.value(1)
    else:
        print("Relay off")
        relay.value(0)
    '''
    sleep(0.005)