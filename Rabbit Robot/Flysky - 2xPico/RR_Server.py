#RR_Server
#Importing necessary header files
from machine import Pin, PWM, UART
from time import sleep
from ibus import IBus

#Setting commuincation channel between Flysky and Pico
ibus_in = IBus(1)

#Setting channel, baud rate and pins for communication between Pico to Pico
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

#Defining pins for motors
m1p1 = Pin(4,Pin.OUT)
m1p2 = Pin(3,Pin.OUT)
m1en = PWM(Pin(2))

m2p1 = Pin(8,Pin.OUT)
m2p2 = Pin(7,Pin.OUT)
m2en = PWM(Pin(6))

m3p1 = Pin(12,Pin.OUT)
m3p2 = Pin(11,Pin.OUT)
m3en = PWM(Pin(10))

#Funtion for reading data from Flysky and Sending it to Pico2
no_of_channels=6
command = [0]*no_of_channels
def readval():
    
    global command
    res = ibus_in.read()
    if res[0]:
        for i in range(0,no_of_channels):
            command[i] = IBus.normalize(res[i+1])
    #print(command)
    message=','.join(map(str,command))
    uart.write(message.encode('utf-8'))

    
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
    if command[0] or command[1]: #command[0] and command[1] is x and y motion of joystick
        botmove(-command[0],command[1])
    elif command[3]>80: #command[3] is used for rotating the bot
        botrotate(dir=0)
    elif command[3]<-80:
        botrotate(dir=1)
    else:  
        botstop()
    sleep(0.01)
