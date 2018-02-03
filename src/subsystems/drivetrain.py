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
        self.motor_rf = ctre.WPI_VictorSPX(17)
        self.motor_lb = ctre.WPI_TalonSRX(13)
        self.motor_lf = ctre.WPI_VictorSPX(15)
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
        self.leftError = networktables.NetworkTables.getTable("/TalonL/Error")
        self.rightError = networktables.NetworkTables.getTable("/TalonR/Error")

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

    def initilize_driveForward(self):
        self.zeroEncoders()
        self.motor_rb.configMotionAcceleration(int(self.getEncoderAccel(5)), 0)
        self.motor_lb.configMotionAcceleration(int(self.getEncoderAccel(5)), 0)
        self.motor_rb.configMotionCruiseVelocity(int(self.getEncoderVelocity(5)), 0)
        self.motor_lb.configMotionCruiseVelocity(int(self.getEncoderVelocity(5)), 0)
        # self.motor_rb.configNominalOutputForward(0, 0)
        # self.motor_lb.configNominalOutputForward(0, 0)
        # self.motor_rb.configNominalOutputReverse(0, 0)
        # self.motor_lb.configNominalOutputReverse(0, 0)
        # self.motor_rb.configPeakOutputForward(1, 0)
        # self.motor_lb.configPeakOutputForward(1, 0)
        # self.motor_rb.configPeakOutputReverse(-1, 0)
        # self.motor_lb.configPeakOutputReverse(-1, 0)
        self.motor_rb.selectProfileSlot(0, 0)
        self.motor_lb.selectProfileSlot(0, 0)
        # self.motor_rb.config_kF(0, 0, 0)
        # self.motor_lb.config_kF(0, 0, 0)
        self.motor_rb.config_kP(0, 0.18, 0)
        self.motor_lb.config_kP(0, 0.18, 0)
        self.motor_rb.config_kI(0, 0, 0)
        self.motor_lb.config_kI(0, 0, 0)
        self.motor_rb.config_kD(0, 2, 0)
        self.motor_lb.config_kD(0, 2, 0)

    def execute_driveforward(self):
        self.motor_rb.set(ctre._impl.ControlMode.MotionMagic, self.ratio * -25)
        self.motor_lb.set(ctre._impl.ControlMode.MotionMagic, self.ratio * 25)
        self.drive.feed()

    def isFinished_driveforward(self):
        return False
        sensorPL = self.motor_lb.getSelectedSensorPosition(0)
        return sensorPL > 3.5 * self.ratio


    def end_driveforward(self):
        self.motor_rb.set(0)
        self.motor_lb.set(0)
        # doesn't compensate for deceleration

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

        errorL = self.motor_lb.getClosedLoopError(0)
        errorR = self.motor_rb.getClosedLoopError(0)

        targetR = self.motor_rb.getClosedLoopTarget(0)
        targetL = self.motor_lb.getClosedLoopTarget(0)

        voltageL2 = self.motor_lb.getBusVoltage()
        voltageR2 = self.motor_rb.getBusVoltage()

        iErrorL = self.motor_lb.getIntegralAccumulator(0)
        iErrorR = self.motor_rb.getIntegralAccumulator(0)

        self.leftError.putNumber("Value", errorL)
        self.rightError.putNumber("Value", errorR)

        self.leftError.putNumber("I", iErrorL)
        self.rightError.putNumber("I", iErrorR)

        self.leftError.putNumber("Voltage", voltageL2)
        self.rightError.putNumber("Voltage", voltageR2)

        self.leftError.putNumber("Target", targetL)
        self.rightError.putNumber("Target", targetR)

        if self.logger is not None:
            self.logger.writerow([t, angle, sensorPL, sensorPR, sensorVL, sensorVR, voltageL, voltageR, self.mode])




