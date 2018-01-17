import wpilib
from robotpy_ext.common_drivers import navx
import ctre
from wpilib.command.subsystem import Subsystem


class Drivetrain(Subsystem):

    def __init__(self):
        super().__init__('Drivetrain')

        self.motor_rb = ctre.WPI_TalonSRX(2)
        self.motor_lb = ctre.WPI_TalonSRX(1)
        self.motor_rf = ctre.WPI_TalonSRX(3)
        self.motor_lf = ctre.WPI_TalonSRX(4)
        self.motors = [self.motor_rb, self.motor_lb, self.motor_rf, self.motor_lf]
        self.drive = wpilib.drive.DifferentialDrive(self.motor_rb, self.motor_lb, self.motor_rf, self.motor_lf)
        self.navx = navx.AHRS.create_spi()

    def drive(self, joystick):

        self.drive.arcadeDrive(joystick)
