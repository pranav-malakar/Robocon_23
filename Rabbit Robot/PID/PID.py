class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.last_error = 0
        self.integral = 0

    def update(self, process_variable):
        error = self.setpoint - process_variable
        proportional = self.Kp * error
        self.integral += self.Ki * error
        derivative = self.Kd * (error - self.last_error)
        control_variable = proportional + self.integral + derivative
        self.last_error = error
        return control_variable

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        #self.integral = 0
        #self.last_error = 0

