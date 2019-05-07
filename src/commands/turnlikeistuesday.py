import wpilib.command
import ctre


class Turnlikeistuesday(wpilib.command.Command):
    ratio = 888

    def __init__(self, position):
        super().__init__("Turnlikeistuesday")
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.position = position

    def initialize(self):
        self.drivetrain.zeroNavx()
        self.drivetrain.zeroEncoders()
        self.drivetrain.logger_enabled = True

    def execute(self):
        self.drivetrain.turn_left(1.0)
        
    def isFinished(self):
        return False

    def end(self):
        self.drivetrain.logger_enabled = False
        self.drivetrain.off()
