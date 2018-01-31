import wpilib.command
from oi import getJoystick
from subsystems.drivetrain import Drivetrain

class Drive(wpilib.command.Command):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__('Drive')
        self.drivetrain = drivetrain
        self.requires(self.drivetrain)

    def initialize(self):
        self.drivetrain.motor_lb.configOpenLoopRamp(2, 0)
        self.drivetrain.motor_rb.configOpenLoopRamp(2, 0)

    def execute(self):
        self.drivetrain.mode = "Drive"
        joystick = getJoystick()
        fw = joystick.getRawAxis(1)
        lr = joystick.getRawAxis(4)
        self.drivetrain.drive.arcadeDrive(fw, lr)

    def isFinished(self):
        return False
