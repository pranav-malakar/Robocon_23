#Importing necessary header files
import Adafruit_PCA9685

#Initializing 2 x PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
PCA1 = Adafruit_PCA9685.PCA9685(0x40)
PCA1.set_pwm_freq(SET_FREQ)
PCA2 = Adafruit_PCA9685.PCA9685(0x41)
PCA2.set_pwm_freq(SET_FREQ)

while True:
    
    PCA1.set_pwm(0, 0, 4095) #high 
    PCA1.set_pwm(1, 0, 0) #low
    PCA1.set_pwm(2, 0, 4095)
    
    PCA2.set_pwm(3, 0, 4095) 
    PCA2.set_pwm(4, 0, 0)
    PCA2.set_pwm(5, 0, 4095)
