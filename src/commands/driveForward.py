import wpilib.command
import ctre


class DriveForward(wpilib.command.Command):
    ratio = 888

    def __init__(self, position):
        super().__init__("DriveForward")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        #self.drivetrain.motor_lb.setInverted(True)
        self.position = position

    def initialize(self):
       self.drivetrain.initilize_driveForward()


    def execute(self):
        self.drivetrain.execute_driveforward(self.position, -self.position)



    def isFinished(self):
        if self.drivetrain.isFinished_driveforward(self.position):
            return True

    def end(self):
        self.drivetrain.end_driveforward()




