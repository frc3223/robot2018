from robotpy_ext.common_drivers import navx
import wpilib

class turnLeft(wpilib.command.Command):
    def __init__(self, degrees):
       super().__init__("autoNavx")
       self.requires(self.getRobot().drivetrain)
       self.drivetrain = self.getRobot().drivetrain
       self.degrees = degrees
       self.power = 0
       self.done = False

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.navx.reset()

    def execute(self):
        self.drivetrain.getAngle()
        if self.drivetrain.getAngle() < self.degrees:
            self.Rpower = 0
            self.Lpower = 0.7
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
        elif self.drivetrain.getAngle() >= self.degrees:
            self.Rpower = 0
            self.Lpower = 0
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
            self.done = True

    def isFinished(self):
        if (self.done and abs(self.drivetrain.motor_lb.getSelectedSensorVelocity(0)) <= 30 and abs(self.drivetrain.motor_rb.getSelectedSensorVelocity(0)) <= 30):
            self.done = False
            return True
        else:
            return False



class turnRight(wpilib.command.Command):
    def __init__(self, degrees):
        super().__init__("autoNavx")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        self.degrees = degrees
        self.done = False

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.navx.reset()

    def execute(self):

        if self.navx.getAngle() < self.degrees:
            self.Rpower = 0.8
            self.Lpower = 0
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
        elif self.navx.getAngle() >= self.degrees:
            self.Rpower = 0
            self.Lpower = 0
            self.drivetrain.motor_rb.set(self.Rpower)
            self.drivetrain.motor_lb.set(self.Lpower)
            self.done = True

    def isFinished(self):
        if (self.done and abs(self.drivetrain.motor_lb.getSelectedSensorVelocity(0)) <= 30 and abs(
                self.drivetrain.motor_rb.getSelectedSensorVelocity(0)) <= 30):
            self.done = False
            return True
        else:
            return False
