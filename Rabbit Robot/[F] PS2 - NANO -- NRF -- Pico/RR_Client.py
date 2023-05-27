#RR_Client
#Importing necessary header files
from machine import Pin, PWM, UART
from time import sleep

#Setting channel, baud rate and pins for communication between Pico to Pico
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

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

#Defining pins for motors
m1p1 = Pin(2,Pin.OUT)
m1p2 = Pin(4,Pin.OUT)
m1en = PWM(Pin(3,Pin.OUT))

m2p1 = Pin(8,Pin.OUT)
m2p2 = Pin(10,Pin.OUT)
m2en = PWM(Pin(9,Pin.OUT))

m3p1 = Pin(13,Pin.OUT)
m3p2 = Pin(15,Pin.OUT)
m3en = PWM(Pin(14,Pin.OUT))

#Function for reading data from Pico2
no_of_channels=4
command = [0]*no_of_channels
def readval():
    
    global command
    #We are using exceptional handling so as to avoid unicode error
    if uart.any():
        try:
            message_bytes = uart.read()
            message = message_bytes.decode('utf-8')
            #Checking if the correct data is recieved
            if message.find(',')!=-1:
                command = list(map(int,message.split(",")))
                #print(command)
        except:
            pass
    
#This function is used for moving the bot
def botmove(Vx,Vy): #Vx is the x component and Vy is the y component
    
    #Theses values are derived using inverse kinematics
    m1speed=int(250*((-0.5*Vx)+(0.5*Vy)))
    m2speed=int(250*((-0.5*Vx)+(-0.5*Vy)))
    m3speed=int(250*((1*Vx)+(0*Vy)))
    
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
    m1en.duty_u16(8000)
    
    m2p1.value(not dir)
    m2p2.value(dir)
    m2en.duty_u16(8000)
    
    m3p1.value(not dir)
    m3p2.value(dir)
    m3en.duty_u16(8000)

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
    if command[0] or command[1]: #Right Joystick is used for x and y motion of the bot
        botmove(-command[0],command[1])
    elif command[2]: #L1 is used for rotating the bot clockwise
        botrotate(dir=1)
    elif command[3]: #R1 is used for rotating the bot anti-clockwise
        botrotate(dir=0)
    else:  
        botstop()
    sleep(0.01)

