from easy_comms import Easy_comms
from time import sleep
from machine import Pin
import json

com1 = Easy_comms(0,9600)
command={'ch1':0,'ch2':0}

while True:
    com1.send(str(json.dumps(command)))
    sleep(0.001)
     
