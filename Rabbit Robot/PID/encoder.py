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
        
        current_tick = self.total_ticks
        self.rot_speed = (current_tick - self.previous_ticks) /self.PPR * 60 * 1000 / self.rpm_time_interval
        self.RPM = self.rot_speed / 2  # divide by 2 to account for quadrature encoding
        self.previous_ticks = current_tick

    def start_RPM_timer(self):
        self.timer.init(freq=1000 / self.rpm_time_interval,mode=Timer.PERIODIC, callback=self.calculate_RPM)

    def stop_RPM_timer(self):
        self.timer.deinit()

    def getRPM(self):
        return self.RPM

    def getEncoderTick(self):
        return self.total_ticks / self.PPR

if __name__ == "__main__":
    

    encoder_1 = Encoder(27, 28)
    encoder_1.start_RPM_timer()

    encoder_2 = Encoder(26, 22)
    encoder_2.start_RPM_timer()

    encoder_3 = Encoder(21, 20)
    encoder_3.start_RPM_timer()

    timee = Timer()


    def printEncoder(a):
        print(f"{encoder_1.total_ticks: >4} {encoder_1.RPM:.2f}, {encoder_2.total_ticks: >4} {encoder_2.RPM:.2f}, {encoder_3.total_ticks: >4} {encoder_3.RPM:.2f}")

    timee.init(freq=10, mode=Timer.PERIODIC, callback=printEncoder)
    while True:
        pass
