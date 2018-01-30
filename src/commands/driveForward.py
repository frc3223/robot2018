import wpilib.command


class DriveForward(wpilib.command.Command):
    ratio = 888

    def __init__(self):
        super().__init__("DriveForward")
        self.requires(self.getRobot().drivetrain)

    def initialize(self):
        self.getRobot().drivetrain.zeroEncoders()
        self.getRobot().drivetrain.motor_rb.configMotionAcceleration(self.getRobot.drivetrain.getEncoderAccel(1), 0)
        self.getRobot().drivetrain.motor_lb.configMotionAcceleration(self.getRobot.drivetrain.getEncoderAccel(1), 0)
        self.getRobot().drivetrain.motor_rb.configMotionCruiseVelocity(self.getRobot.drivetrain.getEncoderVelocity(1), 0)
        self.getRobot().drivetrain.motor_lb.configMotionCruiseVelocity(self.getRobot.drivetrain.getEncoderVelocity(1), 0)

    def execute(self):
        self.getRobot().drivetrain.drive.arcadeDrive(-0.4,0)

    def isFinished(self):
        sensorPL = self.getRobot().drivetrain.motor_lb.getSelectedSensorPosition(0)

        return sensorPL > 3.5*self.ratio
        # doesn't compensate for deceleration




