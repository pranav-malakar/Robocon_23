#Importing necessary header files
import Adafruit_PCA9685
import time

#Defining pins for motors
m1p1 = 1
m1p2 = 3
m1en = 2

m2p1 = 5
m2p2 = 7
m2en = 6

m3p1 = 9
m3p2 = 11
m3en = 10

m4p1 = 13
m4p2 = 15
m4en = 14

#Initializing 1 x PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
PCA9685 = Adafruit_PCA9685.PCA9685()
PCA9685.set_pwm_freq(SET_FREQ)
flag=0

#Testing the connections and motors by running them in both directions
while True:

    time.sleep(10)
    if flag==0:

        PCA9685.set_pwm(m1p1, 0, 4095) #high 
        PCA9685.set_pwm(m1p2, 0, 0) #low
        PCA9685.set_pwm(m1en, 0, 400)

        PCA9685.set_pwm(m2p2, 0, 4095) 
        PCA9685.set_pwm(m2p1, 0, 0)
        PCA9685.set_pwm(m2en, 0, 350)

        PCA9685.set_pwm(m3p2, 0, 4095)  
        PCA9685.set_pwm(m3p1, 0, 0) 
        PCA9685.set_pwm(m3en, 0, 400)

        PCA9685.set_pwm(m4p2, 0, 4095)  
        PCA9685.set_pwm(m4p1, 0, 0) 
        PCA9685.set_pwm(m4en, 0, 420)

        time.sleep(5)

    PCA9685.set_pwm(m1p1, 0, 4095) 
    PCA9685.set_pwm(m1p2, 0, 4095) 
    PCA9685.set_pwm(m1en, 0, 0)

    PCA9685.set_pwm(m2p1, 0, 4095) 
    PCA9685.set_pwm(m2p2, 0, 4095) 
    PCA9685.set_pwm(m2en, 0, 0)

    PCA9685.set_pwm(m3p2, 0, 4095) 
    PCA9685.set_pwm(m3p1, 0, 4095) 
    PCA9685.set_pwm(m3en, 0, 0)

    PCA9685.set_pwm(m4p1, 0, 4095) 
    PCA9685.set_pwm(m4p2, 0, 4095) 
    PCA9685.set_pwm(m4en, 0, 0)

    time.sleep(2)

    if flag==0:

        PCA9685.set_pwm(m1p2, 0, 4095) 
        PCA9685.set_pwm(m1p1, 0, 0)
        PCA9685.set_pwm(m1en, 0, 400)

        PCA9685.set_pwm(m2p1, 0, 4095) 
        PCA9685.set_pwm(m2p2, 0, 0)
        PCA9685.set_pwm(m2en, 0, 350)

        PCA9685.set_pwm(m3p1, 0, 4095) 
        PCA9685.set_pwm(m3p2, 0, 0)
        PCA9685.set_pwm(m3en, 0, 400)

        PCA9685.set_pwm(m4p1, 0, 4095) 
        PCA9685.set_pwm(m4p2, 0, 0)
        PCA9685.set_pwm(m4en, 0, 420)

        time.sleep(5)
        flag=1

    PCA9685.set_pwm(m1p1, 0, 4095)
    PCA9685.set_pwm(m1p2, 0, 4095) 
    PCA9685.set_pwm(m1en, 0, 0)

    PCA9685.set_pwm(m2p1, 0, 4095)
    PCA9685.set_pwm(m2p2, 0, 4095) 
    PCA9685.set_pwm(m2en, 0, 0)

    PCA9685.set_pwm(m3p2, 0, 4095) 
    PCA9685.set_pwm(m3p1, 0, 4095) 
    PCA9685.set_pwm(m3en, 0, 0)

    PCA9685.set_pwm(m4p1, 0, 4095) 
    PCA9685.set_pwm(m4p2, 0, 4095) 
    PCA9685.set_pwm(m4en, 0, 0)

    time.sleep(2)
