#from ibus import IBus
from time import sleep
from Motor import MotorDriver
from Encoder import Encoder
from machine import Pin, PWM, UART, Timer

#ibus_in = IBus(1)  #Setting commuincation channel between Flysky and Pico

sleep(0)

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# rename motors according to its positoin in bot 
motor_1 = MotorDriver(4,3,2)
motor_2 = MotorDriver(8,7,6)
motor_3 = MotorDriver(12,11,10)

motor_1.set_pwm(0)
motor_2.set_pwm(0)
motor_2.set_pwm(0)

encoder_3 = Encoder(27, 28)
encoder_2 = Encoder(26, 24)
encoder_1 = Encoder(21, 20)

encoder_1.start_RPM_timer()
encoder_2.start_RPM_timer()
encoder_3.start_RPM_timer()

def printEncoderCallBack(t):
    print(f"Encoder 1 [Tick {encoder_1.getEncoderTick():f} RPM {encoder_1.getRPM() }] | Encoder 2 [Tick {encoder_2.getEncoderTick():f} RPM {encoder_2.getRPM() }] | Encoder 3 [Tick {encoder_3.getEncoderTick():f} RPM {encoder_3.getRPM() }]\r", end="")

printTimer = Timer()
printTimer.init(mode=Timer.PERIODIC, freq=10, callback=printEncoderCallBack)

no_of_channels=6
command = [0]*no_of_channels
def readReciver():
    global command
    res = ibus_in.read()
    if res[0]:
        for i in range(0,no_of_channels):
            command[i] = IBus.normalize(res[i+1])
    #print(command)
    message=','.join(map(str,command))
    #uart.write(message.encode('utf-8'))
    
#This function is used for moving the bot
def botmove(Vx,Vy): #Vx is the x component and Vy is the y component
    
    #Theses values are derived using inverse kinematics
    motor_1_pwm=int(640*((-0.5*Vx)+(0.5*Vy)))
    motor_2_pwm=int(640*((-0.5*Vx)+(-0.5*Vy)))
    motor_3_pwm=int(640*((1*Vx)+(0*Vy)))
    
    #Checking the individual motor values
    print(f"M1-> {motor_1_pwm} M2-> {motor_2_pwm} M3-> {motor_3_pwm}")

    motor_1.set_pwm(0)
    motor_2.set_pwm(0)
    motor_2.set_pwm(0)
    
def botstop():
    motor_1.stop()
    motor_2.stop()
    motor_3.stop()

while True:
    motor_1.set_pwm(10)
    motor_2.set_pwm(10)
    motor_3.set_pwm(10)

    #readReciver()
    '''
    if command[0] or command[1]: #command[0] and command[1] is x and y motion of joystick 
        botmove(-command[0],command[1])
    else:  
        botstop()
    '''    
    sleep(0.01) 



