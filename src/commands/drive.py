import wpilib.command
from oi import getJoystick

class Drive(wpilib.command.Command):
    def __init__(self):
        super().__init__('Drive')
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)

    def initialize(self):
        self.drivetrain.motor_lb.configOpenLoopRamp(0.2, 0)
        self.drivetrain.motor_rb.configOpenLoopRamp(0.2, 0)

    def execute(self):
        joystick = getJoystick()
        fw = joystick.getRawAxis(1)
        lr = joystick.getRawAxis(0)

        fw2 = joystick.getRawAxis(5)
        lr2 = joystick.getRawAxis(4)

        if abs(fw2) > 0.2 or abs(lr2) > 0.2:
             self.drivetrain.drive.arcadeDrive(fw2 * .3, lr2 * .5, squaredInputs=False)
        elif abs(fw) > 0.2 or abs(lr) > 0.2:
            self.drivetrain.drive.arcadeDrive(fw, lr, squaredInputs=False)
        else:
            self.drivetrain.drive.arcadeDrive(0, 0)

    def isFinished(self):
        return False
    '''
    def janky(self):
        joystick = getJoystick()
        if joystick.getPOV(0) == 90:
            self.drivetrain.motor_rb.set(0.40)
            self.drivetrain.motor_lb.set(0.40)
        elif joystick.getPOV(0) == 270:
                self.drivetrain.motor_rb.set(-0.40)
                self.drivetrain.motor_lb.set(-0.40)
        else:
            self.drivetrain.motor_rb.set(0)
            self.drivetrain.motor_lb.set(0)
            '''
