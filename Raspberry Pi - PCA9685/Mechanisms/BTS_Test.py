#Importing necessary header files
import Adafruit_PCA9685
import time

#Defining pins for motors
m1rpwm = 1
m1lpwm = 2
m1en = 3

#Initializing PCA9685 and PWM frequency
SET_FREQ = 100
PCA9685 = Adafruit_PCA9685.PCA9685(0x40)
PCA9685.set_pwm_freq(SET_FREQ)

flag=0

#Enabling directional movement by giving high to R_En and L_en
PCA9685.set_pwm(m1en, 0, 4095)

#Testing the connections and motors by running them in both directions 
while True:
    if flag==0:

        PCA9685.set_pwm(m1lpwm, 0, 4095)
        time.sleep(5)
        PCA9685.set_pwm(m1lpwm, 0, 0)

    time.sleep(2)

    if flag==0:

        PCA9685.set_pwm(m1rpwm, 0, 4095)     
        time.sleep(5)
        PCA9685.set_pwm(m1rpwm, 0, 0)
        flag=1

    break
