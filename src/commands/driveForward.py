import wpilib.command
import ctre


class DriveForward(wpilib.command.Command):
    ratio = 888

    def __init__(self):
        super().__init__("DriveForward")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        #self.drivetrain.motor_lb.setInverted(True)

    def initialize(self):
       self.drivetrain.initilize_driveForward()


    def execute(self):
        self.drivetrain.execute_driveforward()



    def isFinished(self):
        self.drivetrain.isFinished_driveforward()

    def end(self):
        self.drivetrain.end_driveforward()




