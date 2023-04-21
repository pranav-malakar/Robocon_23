from machine import Pin, UART
from ibus import IBus
from time import *

ibus_in = IBus(1)

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
c =[0, 0, 0, 0, 0, 0]

def readval():
    res = ibus_in.read()
    if res[0]:
        c[0] = IBus.normalize(res[1])
        c[1] = IBus.normalize(res[2])
        c[2] = IBus.normalize(res[3])
        c[3] = IBus.normalize(res[4])
        c[4] = IBus.normalize(res[5])
        c[5] = IBus.normalize(res[6])
    
    message = "{0},{1},{2},{3},{4},{5}".format(c[0], c[1], c[2], c[3], c[4], c[5])
    print(message)
    message_bytes = message.encode('utf-8')
    uart.write(message_bytes)
while True:
    readval()
    sleep(0.01)
    
