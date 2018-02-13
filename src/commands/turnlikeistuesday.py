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
        self.drivetrain.initialize_driveTurnlike()

    def execute(self):
        self.drivetrain.execute_turn(self.position)
        
    def isFinished(self):
        return abs(self.drivetrain.navx.getAngle() - self.position) < 7

    def end(self):
        self.drivetrain.uninitialize_driveTurnlike()
        self.drivetrain.off()
