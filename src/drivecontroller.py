from pidcontroller import PIDController

class DriveController(PIDController):
    def __init__(self, Kp, Kd, Ks, Kv, Ka, get_voltage, *args, **kwargs):
        super().__init__(Kp, 0, Kd, *args, **kwargs)

        self.pidInput.getPIDSourceType = lambda:self.PIDSourceType.kRate
        self.Ks = Ks
        self.Kv = Kv
        self.Ka = Ka
        self.accel_setpoint = 0
        self.get_voltage = get_voltage
        self.setOutputRange(-1.0, 1.0)

    def getAccelerationSetpoint(self):
        with self.mutex:
            return self.accel_setpoint

    def setAccelerationSetpoint(self, a):
        with self.mutex:
            self.accel_setpoint = a

    def calculateFeedForward(self):
        velocity = self.getSetpoint()
        accel = self.getAccelerationSetpoint()
        available_voltage = self.get_voltage()

        if available_voltage == 0:
            return 0

        v_sign = 0
        if velocity > 0:
            v_sign = 1
        if velocity < 0:
            v_sign = -1

        ks = v_sign * self.Ks

        required_voltage = ks + self.Ka * accel + self.Kv * velocity

        return required_voltage / available_voltage
