from wpilib.command import Command

class DriveForward(Command):
    def __init__(self, position):
        super().__init__("DriveForward")
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        self.position_ft = position

    def initialize(self):
       self.drivetrain.initialize_driveForward()
       print("initialize")

    def execute(self):
        self.drivetrain.execute_driveforward(self.position_ft, -self.position_ft)
        print("Execute")
    def isFinished(self):
        if self.drivetrain.isFinished_driveforward(self.position_ft):
            return True

    def end(self):
        self.drivetrain.off()
        print("End")




