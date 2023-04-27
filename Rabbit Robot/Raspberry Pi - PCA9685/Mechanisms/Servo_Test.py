#Importing necessary header files
import Adafruit_PCA9685
import time

#Initializing PCA9685 with I2C address and PWM frequency
SET_FREQ = 100
PCA = Adafruit_PCA9685.PCA9685(0x41)
PCA.set_pwm_freq(SET_FREQ)

'''
Initial position of servo-

 /   \
|_____|
|     |
|     |

Final position of servo-

|\___/|
|     |
|     |

'''

#Initializing pins for servo
servo1=0
servo2=2

while True:
    
    PCA.set_pwm(servo1, 0, 605)
    PCA.set_pwm(servo2, 0, 1025)
    time.sleep(2)
    
    #For loop and delay for reducing the soeed of servo
    for i in range(400):
        PCA.set_pwm(servo1, 0, 605+i)
        PCA.set_pwm(servo2, 0, 1025-i)
        time.sleep(0.005)
