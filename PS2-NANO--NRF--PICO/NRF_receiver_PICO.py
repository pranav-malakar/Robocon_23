#RR_Server
#Importing necessary header files
from machine import Pin, PWM, UART, SPI
from time import sleep
#from ibus import IBus
import ustruct as struct
from nrf24l01 import *
from micropython import const

#Setting commuincation channel between Flysky and Pico
#ibus_in = IBus(1)

#Setting channel, baud rate and pins for communication between Pico to Pico
#uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

pipe = (b"\x41\x41\x41\x41\x41") # 'AAAAA' on the ardinuo
cfg = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 14, "ce": 17}   
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)

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

#Defining pins for motors
m1p1 = Pin(19,Pin.OUT)
m1p2 = Pin(3,Pin.OUT)
m1en = PWM(Pin(2))

m2p1 = Pin(8,Pin.OUT)
m2p2 = Pin(18,Pin.OUT)
m2en = PWM(Pin(16))

m3p1 = Pin(12,Pin.OUT)
m3p2 = Pin(11,Pin.OUT)
m3en = PWM(Pin(10))

#Funtion for reading data from Flysky and Sending it to Pico2

no_of_channels=20
JS_values = [0]*no_of_channels
def readval():
    global JS_values
    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            nrf.stop_listening
            nrf.send(0)
            JS_values = list(struct.unpack("20B",buf))
            JS_values[0] -= 132
            JS_values[1] -= 123
            JS_values[2] -= 123
            JS_values[3] -= 123
            #print(JS_values)
    #print(JS_values)
    #message=','.join(map(str,JS_values))
    #uart.write(message.encode('utf-8'))

    
#This function is used for moving the bot
def botmove(Vx,Vy): #Vx is the x component and Vy is the y component
    
    #Theses values are derived using inverse kinematics
    m1speed=int(640*((-0.5*Vx)+(0.5*Vy)))
    m2speed=int(640*((-0.5*Vx)+(-0.5*Vy)))
    m3speed=int(640*((1*Vx)+(0*Vy)))
    
    #Checking the individual motor values
    print("Bot move -",m1speed,m2speed,m3speed)
    
    #If the calculated speed is negative then the direction of the motor is reversed
    m1p1.value(m1speed>=0)
    m1p2.value(m1speed<=0)
    m1en.duty_u16(abs(m1speed))
    
    m2p1.value(m2speed>=0)
    m2p2.value(m2speed<=0)
    m2en.duty_u16(abs(m2speed))
    
    m3p1.value(m3speed>=0)
    m3p2.value(m3speed<=0)
    m3en.duty_u16(abs(m3speed))

#This function is used for rotating the bot
def botrotate(dir):

    if not dir:
        print("Bot Rotate Anti-Clockwise")
    else:
        print("Bot Rotate Clockwise")
    
    m1p1.value(not dir)
    m1p2.value(dir)
    m1en.duty_u16(16000)
    
    m2p1.value(not dir)
    m2p2.value(dir)
    m2en.duty_u16(16000)
    
    m3p1.value(not dir)
    m3p2.value(dir)
    m3en.duty_u16(16000)

#This function is used for stopping the bot
def botstop():
    
    m1p1.value(1)
    m1p2.value(1)
    m1en.duty_u16(0)
    
    m2p1.value(1)
    m2p2.value(1)
    m2en.duty_u16(0)
    
    m3p1.value(1)
    m3p2.value(1)
    m3en.duty_u16(0)
    
    print("Bot stop")

nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, channel = 100, payload_size=20)
nrf.open_rx_pipe(0, pipe)
nrf.set_power_speed(POWER_1, SPEED_2M) # power1 = -12 dBm, speed_2m = 2 mbps
nrf.start_listening()
print('readSensorLoop, waiting for packets... (ctrl-C to stop)')

#Main program starts
while True:
    readval()
    if JS_values[0] or JS_values[1]: #JS_values[0] and JS_values[1] is x and y motion of joystick
        botmove(-JS_values[0],JS_values[1])
    elif JS_values[14]: #JS_values[3] is used for rotating the bot
        botrotate(dir=0)
    elif JS_values[15]:
        botrotate(dir=1)
    else:  
        botstop()
    sleep(0.001)


