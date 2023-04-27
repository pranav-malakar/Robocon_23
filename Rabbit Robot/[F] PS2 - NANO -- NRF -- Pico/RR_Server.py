#RR_Server

#Importing necessary header files
from machine import Pin, PWM, UART, SPI
from time import sleep
import ustruct as struct
from nrf24l01 import *
from micropython import const

#Setting channel, baud rate and pins for communication between Pico to Pico
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

#setting up SPI pins for NRF
pipe = (b"\x41\x41\x41\x41\x41") # 'AAAAA' on the ardinuo
cfg = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 14, "ce": 17}   
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)

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

#Funtion for reading data from NRF and sending to PICO2
no_of_channels=20
JS_values = [0]*no_of_channels
def readval():
    global JS_values
    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            JS_values = list(struct.unpack("20B",buf))
            JS_values[0] -= 132
            JS_values[1] -= 123
            JS_values[2] -= 123
            JS_values[3] -= 123
            #print(JS_values)
    print(JS_values)
    temp=JS_values[0:4]
    temp.append(JS_values[14])
    temp.append(JS_values[15])
    message=','.join(map(str,temp))
    uart.write(message.encode('utf-8'))

nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, channel = 100, payload_size=20)
nrf.open_rx_pipe(0, pipe)
nrf.set_power_speed(POWER_1, SPEED_2M) # power1 = -12 dBm, speed_2m = 2 mbps
nrf.start_listening()
print('readSensorLoop, waiting for packets... (ctrl-C to stop)')

#Main program starts
while True:
    readval()
    sleep(0.005)
