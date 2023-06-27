from time import sleep
from Moter import MotorDriver
from Encoder import Encoder
from PID import PIDController
from machine import Timer



###################### Motor & encoder  ####################
# Initialize the motor and encoder objects
motor = MotorDriver(2, 3, 100)
encoder = Encoder(27, 28)
encoder.start_RPM_timer()
#...........................................................



####################### Wheel PID ##########################
# Initialize the PID controller object
pid = PIDController(Kp=0.1, Ki=0.01, Kd=0.01, setpoint=400)
#............................................................



############################################################
# updating set point while controller is running for testing
setpoint = 0
def mycallback(t):
    global setpoint
    setpoint += 10
    pid.set_setpoint(setpoint)
tim = Timer()
#tim.init(mode=Timer.PERIODIC, freq=1, callback=mycallback)
#............................................................




# Main loop
while True:
    # Read the process variable (RPM)
    process_variable = encoder.RPM
    # Update the PID controller
    control_variable = pid.update(process_variable)
    motor.set_pwm(control_variable)
    print("SP:", pid.setpoint, "PV:", process_variable, "CV:", control_variable)
    #print(encoder.getEncoderTick())
    sleep(0.01)