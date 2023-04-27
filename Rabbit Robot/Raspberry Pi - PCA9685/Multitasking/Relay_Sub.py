#Importing necessary header files
import paho.mqtt.client as mqtt
import time
import json
import Adafruit_PCA9685

#Setting up MQTT client
mqttBroker = "127.0.0.1"
client = mqtt.Client("Shoot")
client.connect(mqttBroker,port=1883)

#Initializing PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
PCA2 = Adafruit_PCA9685.PCA9685(0x41)
PCA2.set_pwm_freq(SET_FREQ)

#Defining pins for relay on PCA2
relayin = 12

def on_message(client, userdata, message):
    
    cmd=str(message.payload.decode("utf-8"))
    jsVal=json.loads(cmd)
    
    if jsVal['t']:
        
        #Triangle is used to send a low signal to the relay
        PCA2.set_pwm(relayin, 0, 0)
        print("Relay on")
        time.sleep(0.5)
        
    else:
        
        print("Relay off")
        PCA2.set_pwm(relayin, 0, 4095)

PCA2.set_pwm(relayin, 0, 4095)

while True:
    
    client.loop_start()
    
    #Subscribing data from the client
    client.subscribe("Relay")
    client.on_message=on_message
    
    client.loop_stop()
    time.sleep(0.02)



