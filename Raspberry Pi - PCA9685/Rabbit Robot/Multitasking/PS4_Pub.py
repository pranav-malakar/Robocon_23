#Importing necessary header files
import pygame
import os
import time
import paho.mqtt.client as mqtt
import json

#Setting up MQTT client
mqttBroker = "127.0.0.1"
client = mqtt.Client("DS4")
client.connect(mqttBroker,port=1883)

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
    
while True:
    
    pygame.init()
    
    if movement == 'Joystick':
        jsVal = getJS()

        #Publishing data for controlling movement of the drive
        d={}
        d['axis1']=jsVal['axis1']
        d['axis2']=jsVal['axis2']
        d['L1']=jsVal['L1']
        d['L2']=jsVal['L2']
        d['R1']=jsVal['R1']
        d['R2']=jsVal['R2']
        data=json.dumps(d)
        client.publish("Drive", data)
        
        #Publishing data for controlling relay
        d={}
        d['t']=jsVal['t']
        data=json.dumps(d)
        if jsVal['t']:
            #This loop is used to take the push of Triangle button as a single command regardless of the duration it is pressed for
            while True:
                temp=getJS()
                if temp['t']:
                    continue
                else:
                    break
        client.publish("Relay", data)
        
        time.sleep(0.05)







