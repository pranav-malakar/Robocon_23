from machine import I2C, Pin
from pca9685 import PCA9685
from motor import DCMotors
from servo import Servos
from ibus import IBus
import utime
'''
                                            CHECK THE FLYSKY REMOTE VALUE FIRST THEN RUN THE RR MAIN CODE
                                            SOMETIMES THE LAB RR SUDDENLY REVERSES VALUES
                IF ALL THE VALUES EXCEPT THE BUTTONS ARE NOT 0 THEN TRIM THE CHANNELS WITH THE PHYSICAL SLIDERS AVAILABLE ON THE SIDES
                            SO, FIRST RUN THE FILES IN THE "flysky_pico" FOLDER THEN CHANGE THE VALUES IN THE MAIN CODE
'''

#ONBOARD LED
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()


SDA = Pin(0)
SCL = Pin(1)
ibus_in = IBus(1)

PCA1_ADDR = 0x41 # PCA 1 ADDRESS
PCA2_ADDR = 0x40 # PCA 2 ADDRESS

i2c=machine.I2C(0,sda=SDA, scl=SCL, freq=125000)
#index position of subsystems in the 'motor.py' file

ring = 3 # RING PICKING MOTOR PIN
LA = 4 #LINEAR ACCTUATOR PIN
SHOOT = 0 #SHOOTING PISTON PIN

#PCA1
I2C_PCA1 = I2C(id=0, sda=SDA, scl=SCL) #INITIALIZING PCA 1
print("device found at address:", hex(I2C_PCA1.scan()[0]))
Motor = DCMotors(i2c=I2C_PCA1, address=PCA1_ADDR, freq=1500)
I2C_PCA1.writeto_mem(PCA1_ADDR, 0x00, b'\x21')
I2C_PCA1.writeto_mem(PCA1_ADDR, 0x01, b'\x04')
I2C_PCA1.writeto_mem(PCA1_ADDR, 0xFE, b'\x79')

#PCA 2
I2C_PCA2 = I2C(id=0, sda=SDA, scl=SCL)
print("device found at address:", hex(I2C_PCA2.scan()[1]))
Servo = Servos(i2c=I2C_PCA2, address=PCA2_ADDR, freq=60)
I2C_PCA2.writeto_mem(PCA2_ADDR, 0x00, b'\x21')
I2C_PCA2.writeto_mem(PCA2_ADDR, 0x01, b'\x04')
I2C_PCA2.writeto_mem(PCA2_ADDR, 0xFE, b'\x79')

#SHOOT

def convert(X, Y, R, P, A, SH):
    
    #DRIVE
    if X or Y:
        
        w_R = int(32*((-0.5*X)+(0.5*Y)))  # speed of LEFT WHEEL
        w_L = int(32*((-0.5*X)+(-0.5*Y)))  # speed of RIGHT WHEEL
        w_B = int(32*((1*X)+(0*Y)))  # speed of BACK WHEEL

        Motor.speed(0, w_L)  # wheel left
        Motor.speed(1, w_R)  # wheel right
        Motor.speed(2, w_B)  # wheel back
        print("WHEEL L: {}, WHEEL R: {}, WHEEL B: {}".format(w_L, w_R, w_B))
        
    elif R > 0: #ROTATE LEFT
        
        Motor.speed(0, 400)  # wheel left
        Motor.speed(1, 400)  # wheel right
        Motor.speed(2, 400)  # wheel back
        print("ROTATE LEFT")
        
    elif R < 0: #ROTATE RIGHT
        
        Motor.speed(0, -400)  # wheel left
        Motor.speed(1, -400)  # wheel right
        Motor.speed(2, -400)  # wheel back
        print("ROTATE RIGHT")
        
    else:
        
        Motor.brake(0)
        Motor.brake(1)
        Motor.brake(2)
        print("BOT STOP")
        
    #PICK UP OF THE RINGS
    if P>35: # P>35 WHILE USING THE 6CH RECEIVER	P>0 WHILE USING THE 10CH RECEIVER
        Motor.speed(ring, 500)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("PICK UP")
    elif P<-35: # P<-35 WHILE USING THE 6CH RECEIVER	P<0 WHILE USING THE 10CH RECEIVER
        Motor.speed(ring, -500)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("PICK DOWN")
    else:
        Motor.brake(ring)
    
    #LINEAR ACTUATOR
    if A>30: # A>30 WHILE USING THE 6CH RECEIVER	S>0 WHILE USING THE 10CH RECEIVER
        Motor.speed(LA, 4095)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("LA EXTEND")
    elif A<-30: #A<-30 WHILE USING THE 6CH RECEIVER	S<0 WHILE USING THE 10CH RECEIVER
        Motor.speed(LA, -4095)  # (GOING UPWARD) PICKING MOTORS ARE CONNECTED TO A SINGLE PIN
        print("LA RETRACT")
    else:
        Motor.brake(LA)
        
    #SERVOS
    #if S>0:
    #    Servo.position(14, degrees=95)
    #    Servo.position(15, degrees=1)
    #elif S<0:
    #    Servo.position(14, degrees=0)
    #    Servo.position(15, degrees=95)
        
    #SHOOTING PISTON
    if SH == -100:
        Servo.piston(SHOOT, 1)
    else:
        Servo.piston(SHOOT, 0)
    
while True:
    res = ibus_in.read()
    # if signal then display immediately
    if (res[0]):
        x_val = IBus.normalize(res[1]) #10ch receiver- ch1		6ch receiver- ch1
        y_val = IBus.normalize(res[2]) #10ch receiver- ch2		6ch receiver- ch2
        rotate_val = IBus.normalize(res[4]) #10ch receiver- ch10		6ch receiver- ch4
        pick  = IBus.normalize(res[3]) #10ch receiver- ch9		6ch receiver- ch3
        acc = IBus.normalize(res[5]) #THE 3 WAY SWITCH 	#10ch receiver- ch6			6ch receiver- ch5
        #ser = IBus.normalize(res[7]) #THE 3 WAY SWITCH 	#10ch receiver- ch7		6ch receiver- can't fit
        shot = IBus.normalize(res[6]) #channel for triggering 	shooting #10ch receiver- ch8		6ch receiver- ch6
        
        # print("Y-AXIS {} X-AXIS {}".format(rl_val,rr_val, end=""))
        convert(x_val, y_val, rotate_val, pick, acc, shot)
    utime.sleep_ms(10)
