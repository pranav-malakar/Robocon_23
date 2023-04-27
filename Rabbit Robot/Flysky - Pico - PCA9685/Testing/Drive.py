from machine import I2C, Pin
from pca9685 import PCA9685
from motor import DCMotors
from ibus import IBus
import utime

PCA_ADDR = 0x41
SDA = Pin(0)
SCL = Pin(1)
#Frequency = 500
i2c=machine.I2C(0,sda=SDA, scl=SCL, freq=125000)
ibus_in = IBus(1)
I2C_PCA = I2C(id=0, sda=SDA, scl=SCL)
print("device found at address:", hex(I2C_PCA.scan()[0]))
# PCA = PCA9685(i2c=I2C_PCA,address=PCA_ADDR)
# PCA.freq(50)
Motor = DCMotors(i2c=I2C_PCA, address=PCA_ADDR, freq=1500)
I2C_PCA.writeto_mem(PCA_ADDR, 0x00, b'\x21')
I2C_PCA.writeto_mem(PCA_ADDR, 0x01, b'\x04')
I2C_PCA.writeto_mem(PCA_ADDR, 0xFE, b'\x79')


def map(x, i_min, i_max, o_min, o_max):
    return max(min(o_max, (x - i_min) * (o_max - o_min) // (i_max - i_min) + o_min), o_min)


def convert(X, Y, RL, RR):
    if X or Y:
        w_R = int(55*((-0.5*X)+(0.5*Y)))  # speed of LEFT WHEEL
        w_L = int(55*((-0.5*X)+(-0.5*Y)))  # speed of RIGHT WHEEL
        w_B = int(55*((1*X)+(0*Y)))  # speed of BACK WHEEL

        Motor.speed(0, map(w_L, -4000, 4000, -4095, 4095))  # wheel left
        Motor.speed(1, map(w_R, -4000, 4000, -4095, 4095))  # wheel right
        Motor.speed(2, map(w_B, -4000, 4000, -4095, 4095))  # wheel back
        print("WHEEL L: {}, WHEEL R: {}, WHEEL B: {}".format(w_L, w_R, w_B))
    elif RL==1:
        Motor.speed(0, -1000)  # wheel left
        Motor.speed(1, -1000)  # wheel right
        Motor.speed(2, -1000)  # wheel back
    elif RR==1:
        Motor.speed(0, 1000)  # wheel left
        Motor.speed(1, 1000)  # wheel right
        Motor.speed(2, 1000)  # wheel back
    else:
        Motor.brake(0)
        Motor.brake(1)
        Motor.brake(2)
while True:
    res = ibus_in.read()
    # if signal then display immediately
    if (res[0]):
        x_val = IBus.normalize(res[1])
        y_val = IBus.normalize(res[2])
        rl_val = IBus.normalize(res[5], type="dial")
        rr_val = IBus.normalize(res[8], type="dial")
        # print("Y-AXIS {} X-AXIS {}".format(rl_val,rr_val, end=""))
        convert(x_val, y_val, rl_val, rr_val)
    utime.sleep_ms(10)