#Importing necessary header files
import paho.mqtt.client as mqtt
import time
import json
import Adafruit_PCA9685

#Setting up MQTT client
mqttBroker = "127.0.0.1"
client = mqtt.Client("Shoot")
client.connect(mqttBroker,port=1883)

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

#Defining pins for motors on PCA2(SFS(Scooping, Flipping ,Shooting))
relay = 0

servo1 = 15
servo2 = 14

flip_mp1 = 6
flip_mp2 = 5
flip_en = 4

#Initializing PCA9685 with I2C address and PWM frequency
SET_FREQ = 60
SFS = Adafruit_PCA9685.PCA9685(0x41)
SFS.set_pwm_freq(SET_FREQ)

def on_message(client, userdata, message):
    
    cmd=str(message.payload.decode("utf-8"))
    jsVal=json.loads(cmd)
    
    if jsVal['t']:
        
        #Triangle is used to send a low signal to the relay
        SFS.set_pwm(relay, 0, 4095)
        print("Relay on")
        time.sleep(0.5)
        SFS.set_pwm(relay, 0, 0)
        print("Relay off")
    
    elif jsVal['s']:

        print("Servo moving")
        #Moving one servo in clockwise direction and the other in anti-clockwise direction
        for i in range(0,240,2):
            SFS.set_pwm(servo1, 0, 200+int((1.15*i)))
            SFS.set_pwm(servo2, 0, 600-i)
            time.sleep(0.01)
        SFS.set_pwm(servo1, 0, 200)
        SFS.set_pwm(servo2, 0, 600)
        print("Servo stop")

    elif jsVal['o']:

        print("Flipping on")
        SFS.set_pwm(flip_mp1, 0, 4095)
        SFS.set_pwm(flip_mp2, 0, 0)
        SFS.set_pwm(flip_en, 0, 3000)
        time.sleep(0.5)
        print("Flipping reverse")
        SFS.set_pwm(flip_mp1, 0, 0)
        SFS.set_pwm(flip_mp2, 0, 4095)
        SFS.set_pwm(flip_en, 0, 3000)
        time.sleep(2)
        SFS.set_pwm(flip_mp1, 0, 4095)
        SFS.set_pwm(flip_mp2, 0, 4095)
        SFS.set_pwm(flip_en, 0, 0)
    
#Giving a high signal to relay and setting the direction of servo 
SFS.set_pwm(relay, 0, 0)
SFS.set_pwm(servo1, 0, 400)
SFS.set_pwm(servo2, 0, 400)
while True:
    client.loop_start()
    
    #Subscribing data from the client
    client.subscribe("Relay")
    client.on_message=on_message
    
    client.loop_stop()
    time.sleep(0.02)


