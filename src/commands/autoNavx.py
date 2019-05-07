import navx
import wpilib

class TurnLeft(wpilib.command.Command):
    def __init__(self, degrees):
       super().__init__("autoNavx")
       self.requires(self.getRobot().drivetrain)
       self.drivetrain = self.getRobot().drivetrain
       self.degrees = -degrees
       self.cutoff = -degrees + 35
       self.power = 0
       self.done = False

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        self.drivetrain.voltage_ramp_off()

    def execute(self):
        print("left turn", self.drivetrain.getAngle(), self.cutoff)
        if self.drivetrain.getAngle() > self.cutoff:
            self.drivetrain.turn_left(0.4)
        elif self.drivetrain.getAngle() >= self.degrees:
            self.Rpower = 0
            self.drivetrain.off()
            self.done = True

    def isFinished(self):
        if self.done and self.drivetrain.wheels_stopped():
            self.done = False
            return True
        else:
            return False



class TurnRight(wpilib.command.Command):
    def __init__(self, degrees):
        super().__init__("Navx Turn Right")
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.degrees = degrees
        self.cutoff = degrees - 10
        self.done = False

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        self.drivetrain.voltage_ramp_off()

    def execute(self):

        if self.drivetrain.getAngle() < self.cutoff:
            self.drivetrain.turn_right(0.4)
        else:
            self.drivetrain.off()
            self.done = True

    def isFinished(self):
        if self.done and self.drivetrain.wheels_stopped():
            self.done = False
            return True
        else:
            return False
