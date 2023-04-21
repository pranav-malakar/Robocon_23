#Importing necessary header files
from easy_comms import Easy_comms
from time import sleep
from machine import Pin
import json

sleep(5)
#Setting pin and baud rate for communication between Pico to Pico
com1 = Easy_comms(0,9600)

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
pick_mp1 = Pin(,Pin.OUT)
pick_mp2 = Pin(,Pin.OUT)
pick_men = PWM(Pin())

la_mp1 = Pin(,Pin.OUT)
la_mp2 = Pin(,Pin.OUT)
la_men = PWM(Pin())

la_state = 0

servo1 = PWM(Pin())
servo2 = PWM(Pin())
'''
'''
flip_mp1 = Pin(,Pin.OUT)
flip_mp2 = Pin(,Pin.OUT)
flip_en = PWM(Pin())
'''

#Funtion for reading data from Pico1
command = {'x1':0 , 'y1':0 , 'x2':0 , 'y2':0 , 'b1':0 , 'b2':0 } 
def readval():
    
    global command
    message = com1.read()
    if message is not None:
        command = json.loads(message)

'''
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
    
#This function is used more movement of linear actuator
def lamotion():

    global la_state
    la_mp1.value(not la_state)
    la_mp2.value(la_state)
    if la_state==0:
        print("Linear Actuator Extend")
    else:
        print("Linear Actuator Retract")
    la_state = not la_state
'''  
#Main program starts
while True:
    
    readval()
    print(command)
    
    sleep(1)
    

