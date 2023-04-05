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

def convert(X, Y, R, P, A):
    
    #DRIVE
    if X or Y:
        
        w_R = int(40*((-0.5*X)+(0.5*Y)))  # speed of LEFT WHEEL
        w_L = int(40*((-0.5*X)+(-0.5*Y)))  # speed of RIGHT WHEEL
        w_B = int(40*((1*X)+(0*Y)))  # speed of BACK WHEEL

        Motor.speed(0, w_L)  # wheel left
        Motor.speed(1, w_R)  # wheel right
        Motor.speed(2, w_B)  # wheel back
        print("WHEEL L: {}, WHEEL R: {}, WHEEL B: {}".format(w_L, w_R, w_B))
        
    elif R > 0: #ROTATE LEFT
        
        Motor.speed(0, -500)  # wheel left
        Motor.speed(1, -500)  # wheel right
        Motor.speed(2, -500)  # wheel back
        print("ROTATE LEFT")
        
    elif R < 0: #ROTATE RIGHT
        
        Motor.speed(0, 500)  # wheel left
        Motor.speed(1, 500)  # wheel right
        Motor.speed(2, 500)  # wheel back
        print("ROTATE RIGHT")
        
    else:
        
        Motor.brake(0)
        Motor.brake(1)
        Motor.brake(2)
        print("BOT STOP")
        
    #PICK UP OF THE RINGS
    if P>0:
        Motor.speed(3, 500)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("PICK UP")
    elif P<0:
        Motor.speed(3, -500)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("PICK DOWN")
    else:
        Motor.brake(3)
    
    #LINEAR ACTUATOR
    if A>0:
        Motor.speed(4, 500)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("LA EXTEND")
    elif A<0:
        Motor.speed(4, -500)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("LA RETRACT")
    else:
        Motor.brake(4)
        
while True:
    res = ibus_in.read()
    # if signal then display immediately
    if (res[0]):
        x_val = IBus.normalize(res[1])
        y_val = IBus.normalize(res[2])
        pick  = IBus.normalize(res[9])
        rotate_val = IBus.normalize(res[10])
        acc = IBus.normalize(res[6]) #THE 3 WAY SWITCH
        #rr_val = IBus.normalize(res[8], type="dial")
        # print("Y-AXIS {} X-AXIS {}".format(rl_val,rr_val, end=""))
        convert(x_val, y_val, rotate_val, pick, acc)
    utime.sleep_ms(10)
