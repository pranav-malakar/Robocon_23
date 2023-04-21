#RR_Server
#Importing necessary header files
from easy_comms import Easy_comms
from machine import Pin, PWM, UART
from time import sleep
from ibus import IBus
import json

#Setting pin and baud rate for communication between Pico to Pico
com1 = Easy_comms(0,9600)

#Setting commuincation channel between Flysky and Pico
ibus_in = IBus(1)

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
m1p1 = Pin(2,Pin.OUT)
m1p2 = Pin(3,Pin.OUT)
m1en = PWM(Pin(4))

m2p1 = Pin(6,Pin.OUT)
m2p2 = Pin(7,Pin.OUT)
m2en = PWM(Pin(8))

m3p1 = Pin(10,Pin.OUT)
m3p2 = Pin(11,Pin.OUT)
m3en = PWM(Pin(12))

#Funtion for reading data from Flysky and Sending it to Pico2
command = {'x1':0 , 'y1':0 , 'x2':0 , 'y2':0 , 'b1':0 , 'b2':0 } 
def readval():
    
    global command
    res = ibus_in.read()
    if res[0]:
        command['x1'] = IBus.normalize(res[1])
        command['y1'] = IBus.normalize(res[2])
        command['x2'] = IBus.normalize(res[3])
        command['y2'] = IBus.normalize(res[4])
        command['b1'] = IBus.normalize(res[5])
        command['b2'] = IBus.normalize(res[6])
        com1.send(str(json.dumps(command)))
        print(command)
    
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

#Main program starts
while True:
    readval()
    sleep(1)

