import wpilib
from wpilib.command.subsystem import Subsystem
from robotpy_ext.common_drivers import navx
import ctre
from commands.drive import Drive
import networktables


class Drivetrain(Subsystem):

    def __init__(self):
        super().__init__('Drivetrain')

        self.motor_rb = ctre.WPI_TalonSRX(1)
        self.motor_rf = ctre.WPI_TalonSRX(17)
        self.motor_lb = ctre.WPI_TalonSRX(13)
        self.motor_lf = ctre.WPI_TalonSRX(15)
        self.motor_rf.follow(self.motor_rb)
        self.motor_lf.follow(self.motor_lb)
        self.motors = [self.motor_rb, self.motor_lb, self.motor_rf, self.motor_lf]
        self.drive = wpilib.drive.DifferentialDrive(self.motor_rb, self.motor_lb)
        self.navx = navx.AHRS.create_spi()

        self.motor_lb.configSelectedFeedbackSensor(ctre._impl.FeedbackDevice.QuadEncoder,0,0)
        self.motor_rb.configSelectedFeedbackSensor(ctre._impl.FeedbackDevice.QuadEncoder, 0, 0)
        self.navx_table = networktables.NetworkTables.getTable('/Sensor/Navx')
        self.leftEncoder_table = networktables.NetworkTables.getTable("/Encoder/Left")
        self.rightEncoder_table = networktables.NetworkTables.getTable("/Encoder/Right")

    def initDefaultCommand(self):
        self.setDefaultCommand(Drive())


    def periodic(self):
        turntoangle = self.navx.getAngle()
        self.navx_table.putNumber('Angle', turntoangle)


        sensorPL = self.motor_lb.getSelectedSensorPosition(0)
        self.leftEncoder_table.putNumber("Position",sensorPL)

        sensorPR = self.motor_rb.getSelectedSensorPosition(0)
        self.rightEncoder_table.putNumber("Position",sensorPR)

        sensorVL = self.motor_lb.getSelectedSensorVelocity(0)
        self.leftEncoder_table.putNumber("Velocity",sensorVL)

        sensorVR = self.motor_rb.getSelectedSensorVelocity(0)
        self.rightEncoder_table.putNumber("Velocity",sensorVR)

