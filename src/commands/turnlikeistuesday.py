import wpilib.command
import ctre


class Turnlikeistuesday(wpilib.command.Command):
    ratio = 888

    def __init__(self, position):
        super().__init__("Turnlikeistuesday")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        #self.drivetrain.motor_lb.setInverted(True)
        self.position = position

    def initialize(self):
        self.drivetrain.initilize_driveForward()

    def execute(self):
        self.drivetrain.execute_turn(self.position)
        
        

    def isFinished(self):
        self.drivetrain.isFinished_driveforward()
    
    def end(self):
        self.drivetrain.end_driveforward()
