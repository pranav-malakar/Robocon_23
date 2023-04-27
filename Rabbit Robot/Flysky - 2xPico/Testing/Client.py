from easy_comms import Easy_comms
from time import sleep
from machine import Pin
import json

com1 = Easy_comms(0,9600)

while True:
    message = com1.read()
    if message is not None:
        command = json.loads(message)
        print(command)
    sleep(0.001)
    
