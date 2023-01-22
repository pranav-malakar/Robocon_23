#Importing necessary header files
import time
import pygame
import os
import RPi.GPIO as GPIO
import Adafruit_PCA9685

#Setting mode for RPi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#Required for setting up DS4
pygame.init()
os.environ["SDL_VIDEORIVER"] = "x11"
controller = pygame.joystick.Joystick(0)

controller.init()

movement = 'Joystick'

buttons = {'x':0, 'o':0, 't':0, 's':0,
           'L1':0, 'R1':0, 'L2':0, 'R2':0,
           'share':0, 'options':0,
           'axis1':0., 'axis2':0., 'axis3':0., 'axis4':0.}
axiss=[0.,0.,0.,0.,0.,0.]




'''
Elephant Robot      
                        ____________________________
                        |                          |
                   M1 |||                          ||| M4
                      |||                          |||
                        |                          |
                        |                          |
                        |                          |
                        |                          |
                        |                          |
                        |                          |
                        |                          |
                        |                          |
                   M2 |||                          ||| M3
                      |||                          |||
                        |__________________________|
        
'''

#Defining pins for motors
m1p1 = 1
m1p2 = 3
m1en = 2

m2p1 = 7
m2p2 = 5
m2en = 6

m3p1 = 9
m3p2 = 11
m3en = 10

m4p1 = 14
m4p2 = 13
m4en = 15

#Initializing 2 x PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
Motor = Adafruit_PCA9685.PCA9685(0x40)
Motor.set_pwm_freq(SET_FREQ)

PCA2 = Adafruit_PCA9685.PCA9685(0x41)
PCA2.set_pwm_freq(SET_FREQ)


#Funtion for reading data from DS4
def getJS(name=''):
    global buttons
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axiss[event.axis] = round(event.value,2)
        elif event.type == pygame.JOYBUTTONDOWN:
            for x,(key,val) in enumerate(buttons.items()):
                if x<10:
                    if controller.get_button(x):buttons[key]=1
        elif event.type == pygame.JOYBUTTONUP:
            for x,(key,val) in enumerate(buttons.items()):
                if x<10:
                    if event.button ==x:buttons[key]=0

    buttons['axis1'], buttons['axis2'], buttons['axis3'], buttons['axis4'] = [axiss[0],axiss[1],axiss[3],axiss[4]]
    if name == '':
        return buttons
    else:
        return buttons[name]


#Main program starts
while True:

    pygame.init()

    if movement == 'Joystick':
        jsVal = getJS()

        if jsVal['axis1'] or jsVal['axis2']:

            Vx=float(jsVal['axis1'])    #Vx is the x component
            Vy=-float(jsVal['axis2'])   #Vy is the y component

            #Theses values are derived using inverse kinematics
            m1speed=int(65*6.369*(Vx-Vy)) #414 
            m2speed=int(65*6.369*(Vx+Vy))
            m3speed=int(65*6.369*(Vx+Vy))
            m4speed=int(65*6.369*(Vx-Vy))

            #Checking the individual motor values
            print(m1speed,m2speed,m3speed,m4speed)

            #If the calculated speed is negative then the direction of the motor is reversed
            if m1speed>=0:
                Motor.set_pwm(m1p1, 0, 4095) #4095 is highest PWM 
                Motor.set_pwm(m1p2, 0, 0) #0 is the lowest PWM
                Motor.set_pwm(m1en, 0, m1speed)
            else:
                Motor.set_pwm(m1p1, 0, 0)
                Motor.set_pwm(m1p2, 0, 4095) 
                Motor.set_pwm(m1en, 0, abs(m1speed))

            if m2speed>=0:
                Motor.set_pwm(m2p1, 0, 4095) 
                Motor.set_pwm(m2p2, 0, 0) 
                Motor.set_pwm(m2en, 0, m2speed)
            else:
                Motor.set_pwm(m2p1, 0, 0) 
                Motor.set_pwm(m2p2, 0, 4095)
                Motor.set_pwm(m2en, 0, abs(m2speed))

            if m3speed>=0:
                Motor.set_pwm(m3p1, 0, 4095) 
                Motor.set_pwm(m3p2, 0, 0)
                Motor.set_pwm(m3en, 0, m3speed)
            else:
                Motor.set_pwm(m3p1, 0, 0) 
                Motor.set_pwm(m3p2, 0, 4095)
                Motor.set_pwm(m3en, 0, abs(m3speed))

            if m4speed>=0:
                Motor.set_pwm(m4p1, 0, 4095) 
                Motor.set_pwm(m4p2, 0, 0)
                Motor.set_pwm(m4en, 0, m4speed)
            else:
                Motor.set_pwm(m4p1, 0, 0) 
                Motor.set_pwm(m4p2, 0, 4095)
                Motor.set_pwm(m4en, 0, abs(m4speed))

            #Checking the joystick values from DS4     
            print("xaxis",jsVal['axis1'])
            print("yaxis",jsVal['axis2'])
            print("Bot move")

        else:

            #If the joystick is not moved then both the pins of the motor will be given a high signal
            Motor.set_pwm(m1p1, 0, 4095) 
            Motor.set_pwm(m1p2, 0, 4095)
            Motor.set_pwm(m1en, 0, 0)

            Motor.set_pwm(m2p1, 0, 4095)  
            Motor.set_pwm(m2p2, 0, 4095)
            Motor.set_pwm(m2en, 0, 0)

            Motor.set_pwm(m3p1, 0, 4095) 
            Motor.set_pwm(m3p2, 0, 4095)
            Motor.set_pwm(m3en, 0, 0)

            Motor.set_pwm(m4p1, 0, 4095) 
            Motor.set_pwm(m4p2, 0, 4095)
            Motor.set_pwm(m4en, 0, 0)

            #Checking if this block is executed or not
            print("Bot stop")

    time.sleep(0.001)
