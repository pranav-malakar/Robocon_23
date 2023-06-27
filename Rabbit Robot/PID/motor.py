# https://github.com/Abhinav-Prajapati
from machine import *
import time


class Encoder:
    def __init__(self, a_pin, b_pin,ppr = 1300/2): #127
        self.a = Pin(a_pin, Pin.IN)
        self.b = Pin(b_pin, Pin.IN)
        self.a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
                   handler=self.update_total_ticks)

        self.total_ticks = 0
        self.last_a = self.a.value()

        self.RPM = 0
        self.PPR = ppr # 127

        self.rot_speed = 0
        self.previous_ticks = 0
        self.rpm_time_interval = 20  # rpm cal interval

        # Calculate moving Average
        self.RPM_buffer_size = 10  # number of previous RPM values to store for moving average
        # initialize RPM buffer with zeros
        self.RPM_buffer = [0] * self.RPM_buffer_size
        self.timer = Timer()

    def update_total_ticks(self, pin):
        a_val = self.a.value()
        b_val = self.b.value()
        if a_val != self.last_a:
            if b_val != a_val:
                self.total_ticks += 1
            else:
                self.total_ticks -= 1
        self.last_a = a_val

    def calculate_RPM(self, timerObj):
        # print("in RPm")
from machine import Pin , PWM
import time

class MotorDriver:
    def __init__(self, fwd_pin, bwd_pin,pwm_pin,max_pwm=50,pwm_range=100,freq=25000):
        
        self.Fwd_pin = Pin(fwd_pin,Pin.OUT)
        self.Bwd_pin = Pin(bwd_pin,Pin.OUT)

        self.motor_pwm =PWM(Pin(pwm_pin))
        self.motor_pwm.freq(freq)
        self.PWM_range=pwm_range = max_pwm
        self.Max_pwm=max_pwm
        
        self.stop()

    def set_pwm(self, pwm):
        pwm = min(abs(pwm), self.Max_pwm) * (1 if pwm >= 0 else -1)
        
        self.Fwd_pin.value(pwm>=0)
        self.Bwd_pin.value(pwm<=0)
        #self.motor_pwm.duty(int(1023 * abs(pwm) / self.pwm_range))
        self.motor_pwm.duty_u16(int(65535*abs(pwm)/self.PWM_range))
        
    def stop(self):
        self.Fwd_pin.value(0)
        self.Bwd_pin.value(0)
        self.motor_pwm.duty_u16(0)


if __name__ == "__main__":

    moter_1 = MotorDriver(4,3,2)
    moter_2 = MotorDriver(8,7,6)
    moter_3 = MotorDriver(12,11,10)
    
    for i in range(30):
        
        moter_1.set_pwm(i)
        moter_2.set_pwm(i)
        moter_3.set_pwm(i)
        time.sleep(0.05)

    moter_1.stop()
    moter_2.stop()
    moter_3.stop()
    time.sleep(2)

    for i in range(30):
        moter_1.set_pwm(-i)
        moter_2.set_pwm(-i)
        moter_3.set_pwm(-i)
        time.sleep(0.05)

    moter_1.stop()
    moter_2.stop()
    moter_3.stop()

    time.sleep(2)
