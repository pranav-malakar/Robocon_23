'''
Observations-

Without Multi-Threading and Multi-Processing, the CPU usage is initially 50% and after 20 secs it settles down to 42%.

Multi-Threading- The CPU usage is initally 100% and after 20 secs it settles down to 37%. 
                 The lag is visible when receiving input from DS4. When the signal should be received immediately, 
                 each pin is given a high or low signal one after the other. Although the the signal is recieved 
                 immediately when the 'time.sleep()' is triggered in 'shoot' function. When 'time.sleep()' ends, the
                 situation returns to how it was before.
                 
Multi-Processing- The CPU usage is initally 100% and after 20 secs it settles down to 66%. 
                  The lag is so massive that it takes around 2-3 seconds to send one signal and after that no change is
                  observed even when the signal is sent from DS4. Although the the signal is recieved immediately when 
                  the 'time.sleep()' is triggered in 'shoot' function. When 'time.sleep()' ends, the situation returns 
                  to how it was before.
                  
Conclusion- Possibly taking input from DS4 is expensive for CPU.

'''

#Importing necessary header files
import time
import pygame
import os
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import multiprocessing #Import threading for implementing multithreading

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

Rabbit Robot      

                        |                          |
                        |                          |
                        |                          |
                        |                          |
                        |                          |
                   M2 |||                          ||| M1
                      |||                          |||
                        |__________________________|
                                    ----
                                    ----
                                     M3
                                     
        
'''

#Defining pins for motors on PCA1(Motor)
m1p1 = 1
m1p2 = 3
m1en = 2

m2p1 = 5
m2p2 = 7
m2en = 6

m3p1 = 9
m3p2 = 11
m3en = 10

#Defining pins for relay on PCA2
relayin = 12

#Initializing 2 x PCA9685 with I2C address0 and PWM frequency
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
    

#Main program starts, giving a high signal

flag=0

#Function for controlling drive
def drive():
    
    while True:
        pygame.init()
        
        if movement == 'Joystick':
            jsVal = getJS()
        
            if jsVal['axis1'] or jsVal['axis2'] or jsVal['L2'] or jsVal['R2'] or jsVal['L1'] or jsVal['R1']:
                
                if jsVal['axis1'] or jsVal['axis2']:
                    
                    #These values are the x, y movement of the left joystick
                    Vx=float(jsVal['axis1'])    #Vx is the x component
                    Vy=-float(jsVal['axis2'])   #Vy is the y component

                    #Theses values are derived using inverse kinematics
                    m1speed=int(700*((-0.5*Vx)+(0.5*Vy)))
                    m2speed=int(700*((-0.5*Vx)+(-0.5*Vy)))
                    m3speed=int(700*((1*Vx)+(0*Vy)))

                    #Checking the individual motor values
                    print(m1speed,m2speed,m3speed)
                    
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

                        #Checking the joystick values from DS4     
                        print("xaxis",jsVal['axis1'])
                        print("yaxis",jsVal['axis2'])
                        print("Bot move")
                
                elif jsVal['L2']:

                    #L2 rotates the bot anti-clockwise
                    Motor.set_pwm(m1p1, 0, 4095) 
                    Motor.set_pwm(m1p2, 0, 0)
                    Motor.set_pwm(m1en, 0, 350)
                    
                    Motor.set_pwm(m2p1, 0, 4095)  
                    Motor.set_pwm(m2p2, 0, 0)
                    Motor.set_pwm(m2en, 0, 350)
                    
                    Motor.set_pwm(m3p1, 0, 4095) 
                    Motor.set_pwm(m3p2, 0, 0)
                    Motor.set_pwm(m3en, 0, 350)
                    
                    print("Bot Rotate Anti-Clockwise")
                
                elif jsVal['R2']:
                    
                    #R2 rotates the bot clockwise
                    Motor.set_pwm(m1p1, 0, 0) 
                    Motor.set_pwm(m1p2, 0, 4095)
                    Motor.set_pwm(m1en, 0, 350)
                    
                    Motor.set_pwm(m2p1, 0, 0)  
                    Motor.set_pwm(m2p2, 0, 4095)
                    Motor.set_pwm(m2en, 0, 350)
                    
                    Motor.set_pwm(m3p1, 0, 0) 
                    Motor.set_pwm(m3p2, 0, 4095)
                    Motor.set_pwm(m3en, 0, 350) 
                    
                    print("Bot Rotate Clockwise")
                
                elif jsVal['L1']:
                    
                    #L1 drifts the bot towards left side
                    Motor.set_pwm(m1p1, 0, 4095) 
                    Motor.set_pwm(m1p2, 0, 0)
                    Motor.set_pwm(m1en, 0, 350)
                    
                    Motor.set_pwm(m2p1, 0, 0)  
                    Motor.set_pwm(m2p2, 0, 4095)
                    Motor.set_pwm(m2en, 0, 350)
                    
                    Motor.set_pwm(m3p1, 0, 0) 
                    Motor.set_pwm(m3p2, 0, 4095)
                    Motor.set_pwm(m3en, 0, 350)

                    print("Left Drift")
                
                elif jsVal['R1']:
                    
                    #R1 drifts the bot towards right side
                    Motor.set_pwm(m1p1, 0, 4095)
                    Motor.set_pwm(m1p2, 0, 0)
                    Motor.set_pwm(m1en, 0, 350)
                    
                    Motor.set_pwm(m2p1, 0, 0)  
                    Motor.set_pwm(m2p2, 0, 4095)
                    Motor.set_pwm(m2en, 0, 350)
                    
                    Motor.set_pwm(m3p1, 0, 4095) 
                    Motor.set_pwm(m3p2, 0, 0)
                    Motor.set_pwm(m3en, 0, 350)                 

                    print("Right Drift")
                
            else:

                #If the joystick is not moved or L1,R1,L2,R2 are not pressed then both the pins of the motor will be given a high signal
                Motor.set_pwm(m1p1, 0, 4095) 
                Motor.set_pwm(m1p2, 0, 4095)
                Motor.set_pwm(m1en, 0, 0)
                
                Motor.set_pwm(m2p1, 0, 4095)  
                Motor.set_pwm(m2p2, 0, 4095)
                Motor.set_pwm(m2en, 0, 0)
                
                Motor.set_pwm(m3p1, 0, 4095) 
                Motor.set_pwm(m3p2, 0, 4095)
                Motor.set_pwm(m3en, 0, 0) 

                #Checking if this block is executed or not
                print("Bot stop")    
            
#Function for controlling relay
def shoot():

    while True:
        pygame.init()
        
        if movement == 'Joystick':
            jsVal = getJS()
            
            if jsVal['t']:
                while True:
                    temp = getJS()
                    if temp['t']:
                        continue
                    else:
                        break 

                #Triangle is used to send a low signal to the relay
                PCA2.set_pwm(relayin, 0, 0)
                #flag=15
                print("Relay on")
                
                time.sleep(5)
                
                #After 5 secs, the relay is given a high signal
                PCA2.set_pwm(relayin, 0, 4095)
                print("Relay off")

if __name__ =="__main__":
    p1 = multiprocessing.Process(target=drive) #Replace multiprocessing.Process by threading.Thread for implementing multithreading
    p2 = multiprocessing.Process(target=shoot) #Replace multiprocessing.Process by threading.Thread for implementing multithreading
    p1.start()
    p2.start()
    p1.join()
    p2.join()
                
