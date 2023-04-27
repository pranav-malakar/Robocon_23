#RR_Client
#Importing necessary header files
from machine import Pin, UART, PWM
from time import sleep

#Setting pin and baud rate for communication between Pico to Pico

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

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
pick_men = PWM(Pin(7))

la_mp1 = Pin(4,Pin.OUT)
la_mp2 = Pin(3,Pin.OUT)
la_men = PWM(Pin(2))

#la_state = 0

'''
servo1 = PWM(Pin())
servo2 = PWM(Pin())

flip_mp1 = Pin(10,Pin.OUT)
flip_mp2 = Pin(11,Pin.OUT)
flip_en = PWM(Pin(12))
'''

#Funtion for reading data from Pico1
no_of_channels=6
command = [0]*no_of_channels

def readval():
    
    global command
    if uart.any():
        try:
            message_bytes = uart.read()
            message = message_bytes.decode('utf-8')
            if message.find(',')!=-1:
                command = list(map(int,message.split(",")))
                #print(command)
        except:
            pass            

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
