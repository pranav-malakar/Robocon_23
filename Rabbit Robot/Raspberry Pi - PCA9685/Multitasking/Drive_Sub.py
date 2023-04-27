#Importing necessary header files
import paho.mqtt.client as mqtt
import time
import json
import Adafruit_PCA9685

#Setting up MQTT client
mqttBroker = "127.0.0.1"
client = mqtt.Client("Move")
client.connect(mqttBroker,port=1883)

#Initializing PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
Motor = Adafruit_PCA9685.PCA9685(0x40)
Motor.set_pwm_freq(SET_FREQ)

#Defining pins for motors on PCA1(Motor)
m1p1 = 0
m1p2 = 1
m1en = 2

m2p1 = 4
m2p2 = 5
m2en = 6

m3p1 = 8
m3p2 = 9
m3en = 10

def on_message(client, userdata, message):
    
    cmd=str(message.payload.decode("utf-8"))
    jsVal=json.loads(cmd)
    
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
            #print("xaxis",jsVal['axis1'])
            #print("yaxis",jsVal['axis2'])
    
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

        print("Bot stop")

while True:
    
    client.loop_start()
    
    #Subscribing data from the client
    client.subscribe("Drive")
    client.on_message=on_message
    
    client.loop_stop()
    time.sleep(0.01)


