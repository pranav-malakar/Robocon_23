#Importing necessary header files
import pygame
import os
import time
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import Adafruit_PCA9685

#Setting mode for RPi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setting up MQTT client
mqttBroker = "127.0.0.1"
client = mqtt.Client("DS4")
client.connect(mqttBroker,port=1883)

#Required for setting up DS4
pygame.init()
os.environ["SDL_VIDEORIVER"] = "x11"
os.putenv('DISPLAY',':0.0')
controller = pygame.joystick.Joystick(0)

controller.init()
movement = 'Joystick'
buttons = {'x':0, 'o':0, 't':0, 's':0,
           'L1':0, 'R1':0, 'L2':0, 'R2':0,
           'share':0, 'options':0,
           'axis1':0., 'axis2':0., 'axis3':0., 'axis4':0.,
           'dpadup':0,'dpaddown':0,'dpadleft':0,'dpadright':0,}
axiss=[0.,0.,0.,0.,0.,0.]

'''
Rabbit Robot

M - Motor
LA - Linear Actuator
S - Servo
P - Piston

                             __________________
                             ||______________||
                            //                \\       
                          // ||              || \\
                        //   ||LA1        LA2||   \\          
                     S1 |____||______________||____| S2                          
                        |                          |
                        |__________________________|
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

#Defining pins for motors on PCA1(Motor)
m1p1 = 1
m1p2 = 2
m1en = 0

m2p1 = 5
m2p2 = 6
m2en = 4

m3p1 = 9
m3p2 = 10
m3en = 8

#Initializing PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
Motor = Adafruit_PCA9685.PCA9685(0x40)
Motor.set_pwm_freq(SET_FREQ)

#Funtion for reading data from DS4
def getJS(name=''):
    global buttons
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axiss[event.axis] = round(event.value,3)
        elif event.type == pygame.JOYBUTTONDOWN:
            for x,(key,val) in enumerate(buttons.items()):
                if x<10:
                    if controller.get_button(x):buttons[key]=1
        elif event.type == pygame.JOYBUTTONUP:
            for x,(key,val) in enumerate(buttons.items()):
                if x<10:
                    if event.button ==x:buttons[key]=0  
        elif event.type == pygame.JOYHATMOTION:
            DPAD = controller.get_hat(0) #this is stored in a tuple
            buttons['dpadup'],buttons['dpaddown'],buttons['dpadleft'],buttons['dpadright']=0,0,0,0 
            if(DPAD == (0,1)): buttons['dpadup']=1
            if(DPAD == (0,-1)): buttons['dpaddown']=1 
            if(DPAD == (-1,0)): buttons['dpadleft']=1
            if(DPAD == (1,0)): buttons['dpadright']=1          
    
    
    buttons['axis1'], buttons['axis2'], buttons['axis3'], buttons['axis4'] = [axiss[0],axiss[1],axiss[3],axiss[4]]
    if name == '':
        return buttons
    else:
        return buttons[name]
    
#This function is used for moving the bot
def botmove(Vx,Vy): #Vx is the x component and Vy is the y component
    
    #Theses values are derived using inverse kinematics
    m1speed=int(1500*((-0.5*Vx)+(0.5*Vy)))
    m2speed=int(1500*((-0.5*Vx)+(-0.5*Vy)))
    m3speed=int(1500*((1*Vx)+(0*Vy)))

    #Checking the individual motor values
    print("Bot move - ",m1speed,m2speed,m3speed)
    
    #If the calculated speed is negative then the direction of the motor is reversed
    Motor.set_pwm(m1p1, 0, (m1speed>=0)*4095) #4095 is highest PWM 
    Motor.set_pwm(m1p2, 0, (m1speed<=0)*4095) #0 is the lowest PWM
    Motor.set_pwm(m1en, 0, abs(m1speed))

    Motor.set_pwm(m2p1, 0, (m2speed>=0)*4095)  
    Motor.set_pwm(m2p2, 0, (m2speed<=0)*4095)
    Motor.set_pwm(m2en, 0, abs(m2speed))
    
    Motor.set_pwm(m3p1, 0, (m3speed>=0)*4095)
    Motor.set_pwm(m3p2, 0, (m3speed<=0)*4095)
    Motor.set_pwm(m3en, 0, abs(m3speed))
    
    #Checking the joystick values from DS4     
    #print("xaxis",jsVal['axis1'])
    #print("yaxis",jsVal['axis2'])
           
#This function is used for rotating the bot
def botrotate(dir):

    if not dir:
        print("Bot Rotate Anti-Clockwise")
    else:
        print("Bot Rotate Clockwise")

    Motor.set_pwm(m1p1, 0, (not dir)*4095) 
    Motor.set_pwm(m1p2, 0, dir*4095)
    Motor.set_pwm(m1en, 0, 350)
    
    Motor.set_pwm(m2p1, 0, (not dir)*4095)  
    Motor.set_pwm(m2p2, 0, dir*4095)
    Motor.set_pwm(m2en, 0, 350)
    
    Motor.set_pwm(m3p1, 0, (not dir)*4095) 
    Motor.set_pwm(m3p2, 0, dir*4095)
    Motor.set_pwm(m3en, 0, 350)

'''
#This function is used for drifting the bot
def botdrift(dir):
    
    if not dir:
        print("Left Drift")
    else:
        print("Right Drift")

    Motor.set_pwm(m1p1, 0, 4095)
    Motor.set_pwm(m1p2, 0, 0)
    Motor.set_pwm(m1en, 0, 350)
    
    Motor.set_pwm(m2p1, 0, 0)  
    Motor.set_pwm(m2p2, 0, 4095)
    Motor.set_pwm(m2en, 0, 350)
    
    Motor.set_pwm(m3p1, 0, dir*4095) 
    Motor.set_pwm(m3p2, 0, (not dir)*4095)
    Motor.set_pwm(m3en, 0, 350)
'''

#This function is used for stopping the bot
def botstop():

    Motor.set_pwm(m1p1, 0, 4095) 
    Motor.set_pwm(m1p2, 0, 4095)
    Motor.set_pwm(m1en, 0, 0)
    
    Motor.set_pwm(m2p1, 0, 4095)  
    Motor.set_pwm(m2p2, 0, 4095)
    Motor.set_pwm(m2en, 0, 0)
    
    Motor.set_pwm(m3p1, 0, 4095) 
    Motor.set_pwm(m3p2, 0, 4095)
    Motor.set_pwm(m3en, 0, 0) 

    print("Bot stop")    

#Main program starts
while True:
    
    pygame.init()
    
    if movement == 'Joystick':
        jsVal = getJS()

        if jsVal['axis3'] or jsVal['axis4'] or jsVal['L1'] or jsVal['R1'] or jsVal['dpadup'] or jsVal['dpaddown'] or jsVal['dpadleft'] or jsVal['dpadright']:
            if jsVal['axis3'] or jsVal['axis4']:
                #These values are the x, y movement of the left joystick
                botmove(float(jsVal['axis3']),float(jsVal['axis4']))
            elif jsVal['L1']:
                #L1 rotates the bot anti-clockwise
                botrotate(dir=0)
            elif jsVal['R1']:
                #R1 rotates the bot clockwise
                botrotate(dir=1)
            elif jsVal['dpadup']:
                #dpadup moves the bot upwards with a slow speed
                botmove(0,-0.5)
            elif jsVal['dpaddown']:
                #dpaddown moves the bot downwards with a slow speed
                botmove(0,0.5)   
            elif jsVal['dpadleft']:
                #dpaddown moves the bot in left direction with a slow speed
                botmove(-0.5,0)   
            elif jsVal['dpadright']:
                #dpadup moves the bot in right direction with a slow speed
                botmove(0.5,0)       
        else:
            #If the joystick is not moved or L1,R1 or DPAD buttons are not pressed then both the pins of the motor will be given a high signal
            botstop()

        #Publishing data for controlling relay
        if jsVal['t']:

            d={}
            d['t']=jsVal['t']
            data=json.dumps(d)
            client.publish("Relay",data)
            if jsVal['t']:
                #This loop is used to take the push of Triangle button as a single command regardless of the duration it is pressed for
                while True:
                    temp=getJS()
                    if temp['t']:
                        continue
                    else:
                        break
            #To save the resources, we are only publishing the data when the key is pressed and when the key is not pressed we will only publish the data one time for value '0' 
            d['t']=jsVal['t']
            data=json.dumps(d)
            client.publish("Relay",data)
        
        time.sleep(0.005)
