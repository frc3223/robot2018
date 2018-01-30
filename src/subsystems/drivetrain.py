import wpilib
import csv
from wpilib.command.subsystem import Subsystem
from robotpy_ext.common_drivers import navx
import ctre
from commands.drive import Drive
import networktables


class Drivetrain(Subsystem):
    ''''''

    #: encoder/ft ratio
    ratio = 886.27

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
        self.navx = navx.AHRS.create_spi(update_rate_hz=150)

        self.motor_lb.configSelectedFeedbackSensor(ctre._impl.FeedbackDevice.QuadEncoder,0,0)
        self.motor_rb.configSelectedFeedbackSensor(ctre._impl.FeedbackDevice.QuadEncoder, 0, 0)
        self.navx_table = networktables.NetworkTables.getTable('/Sensor/Navx')
        self.leftEncoder_table = networktables.NetworkTables.getTable("/Encoder/Left")
        self.rightEncoder_table = networktables.NetworkTables.getTable("/Encoder/Right")

        self.motor_lb.setSensorPhase(True)
        self.motor_rb.setSensorPhase(True)

        self.timer = wpilib.Timer()
        self.timer.start()
        self.mode = ""

        self.logger = None

    def initDefaultCommand(self):
        self.setDefaultCommand(Drive())

    def init_logger(self):
        filepath = '/home/lvuser/drivetrain.csv'
        if wpilib.RobotBase.isSimulation():
            filepath = './drivetrain.csv'
        self.logger = csv.writer(open(filepath, 'w'))
        self.logger.writerow(["time", "heading", "enc_pos_l", "enc_pos_r", "enc_vel_l", "enc_vel_r", "voltage_l", "voltage_r", "mode"])

    def zeroEncoders(self):
        self.motor_rb.setSelectedSensorPosition(0, 0, 0)
        self.motor_lb.setSelectedSensorPosition(0, 0, 0)

    def getEncoderVelocity(self, fps):
        return fps*self.ratio/10

    def getEncoderAccel(self, fps2):
        return fps2*self.ratio/10


    def periodic(self):
        t = self.timer.get()
        angle = self.navx.getYaw()
        self.navx_table.putNumber('Angle', angle)


        sensorPL = self.motor_lb.getSelectedSensorPosition(0)
        self.leftEncoder_table.putNumber("Position", sensorPL)

        sensorPR = self.motor_rb.getSelectedSensorPosition(0)
        self.rightEncoder_table.putNumber("Position", sensorPR)

        sensorVL = self.motor_lb.getSelectedSensorVelocity(0)
        self.leftEncoder_table.putNumber("Velocity", sensorVL)

        sensorVR = self.motor_rb.getSelectedSensorVelocity(0)
        self.rightEncoder_table.putNumber("Velocity", sensorVR)

        voltageL = self.motor_lb.get()
        voltageR = self.motor_rb.get()

        if self.logger is not None:
            self.logger.writerow([t, angle, sensorPL, sensorPR, sensorVL, sensorVR, voltageL, voltageR, self.mode])

