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
m1rpwm = 1
m1lpwm = 2
m1en = 3

m2rpwm = 5
m2lpwm = 6
m2en = 7

m3rpwm = 9 
m3lpwm = 10
m3en = 11

m4rpwm = 13
m4lpwm = 14
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
Motor.set_pwm(m1en, 0, 4095)
Motor.set_pwm(m2en, 0, 4095)
Motor.set_pwm(m3en, 0, 4095)
Motor.set_pwm(m4en, 0, 4095)
while True:

    pygame.init()
    
    if movement == 'Joystick':
        jsVal = getJS()
    
        if jsVal['axis1'] or jsVal['axis2']:
            
            Vx=float(jsVal['axis1'])    #Vx is the x component
            Vy=-float(jsVal['axis2'])   #Vy is the y component

            #Theses values are derived using inverse kinematics
            m1speed=int(200*6.369*(Vx-Vy))
            m2speed=int(200*6.369*(Vx+Vy))
            m3speed=int(200*6.369*(Vx+Vy))
            m4speed=int(200*6.369*(Vx-Vy))

            #Checking the individual motor values
            print(m1speed,m2speed,m3speed,m4speed)
            
            #If the calculated speed is negative then the direction of the motor is reversed
            if m1speed>=0:
                Motor.set_pwm(m1lpwm, 0, 0)
                Motor.set_pwm(m1rpwm, 0, m1speed)
            else:
                Motor.set_pwm(m1lpwm, 0, abs(m1speed))
                Motor.set_pwm(m1rpwm, 0, 0)
                
            if m2speed>=0:
                Motor.set_pwm(m2lpwm, 0, 0)
                Motor.set_pwm(m2rpwm, 0, m2speed)
            else:
                Motor.set_pwm(m2lpwm, 0, abs(m2speed))
                Motor.set_pwm(m2rpwm, 0, 0)
                
            if m3speed>=0:
                Motor.set_pwm(m3lpwm, 0, 0)
                Motor.set_pwm(m3rpwm, 0, m3speed)
            else:
                Motor.set_pwm(m3lpwm, 0, abs(m3speed))
                Motor.set_pwm(m3rpwm, 0, 0)
                
            if m4speed>=0:
                Motor.set_pwm(m4lpwm, 0, 0)
                Motor.set_pwm(m4rpwm, 0, m4speed)
            else:
                Motor.set_pwm(m4lpwm, 0, abs(m4speed))
                Motor.set_pwm(m4rpwm, 0, 0)

            #Checking the joystick values from DS4     
            print("xaxis",jsVal['axis1'])
            print("yaxis",jsVal['axis2'])
            print("Bot move")
        
        else:

            #If the joystick is not moved then both pwm pins of the motor will be given a low signal
            Motor.set_pwm(m1lpwm, 0, 0)
            Motor.set_pwm(m1rpwm, 0, 0)

            Motor.set_pwm(m2lpwm, 0, 0)
            Motor.set_pwm(m2rpwm, 0, 0)

            Motor.set_pwm(m3lpwm, 0, 0)
            Motor.set_pwm(m3rpwm, 0, 0)

            Motor.set_pwm(m4lpwm, 0, 0)
            Motor.set_pwm(m4rpwm, 0, 0)
            
            #Checking if this block is executed or not
            print("Bot stop")
                        
    time.sleep(0.001)
