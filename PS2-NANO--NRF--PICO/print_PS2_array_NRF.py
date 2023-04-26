import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import *
from micropython import const

pipe = (b"\x41\x41\x41\x41\x41") # 'AAAAA' on the ardinuo
recvint = 0
cfg = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 14, "ce": 17}   
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)

# def buf_to_arr(buff, fmt, num): #returns an array
#     arr = []
#     size = struct.calcsize(fmt)/num
#     idx = 0 #index
#     for i in range(num):
#         vals = struct.unpack(fmt,buff[ind : ind + size]) # 0th index is start of bytes, goes up 1 index, reads one byte
#         arr.append(vals) 
#         ind += size
#     return arr

JS_values = []

def rx():    
    nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, channel = 100, payload_size=20)

    nrf.open_rx_pipe(0, pipe)
    nrf.set_power_speed(POWER_2, SPEED_2M) # power1 = -12 dBm, speed_2m = 2 mbps
    nrf.start_listening()

    print('readSensorLoop, waiting for packets... (ctrl-C to stop)')

    while True:
        if nrf.any():
            while nrf.any():
                #JS_values = buf_to_arr(nrf.recv(),">20B",20)
                #x,y = struct.unpack("BB",buf)
                JS_values = struct.unpack(">20B",nrf.recv())
                print(JS_values)
                
rx()


