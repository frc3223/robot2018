import wpilib
import wpilib.drive
import csv
from wpilib.command.subsystem import Subsystem
from robotpy_ext.common_drivers import navx
import ctre
from commands.drive import Drive
import networktables
from data_logger import DataLogger


class Drivetrain(Subsystem):
    ''''''

    #: encoder/ft ratio
    ratio = 886.27

    def __init__(self):
        super().__init__('Drivetrain')
        #The set motor controllers for this years robot and how motors are coded
        self.motor_rb = ctre.WPI_TalonSRX(1)
        self.motor_rf = ctre.WPI_VictorSPX(17)
        self.motor_lb = ctre.WPI_TalonSRX(13)
        self.motor_lf = ctre.WPI_VictorSPX(12)
        self.motor_rf.follow(self.motor_rb)
        self.motor_lf.follow(self.motor_lb)
        self.motors = [self.motor_rb, self.motor_lb, self.motor_rf, self.motor_lf]
        self.drive = wpilib.drive.DifferentialDrive(self.motor_rb, self.motor_lb)
        self.navx = navx.AHRS.create_spi()
        self.pdp = wpilib.PowerDistributionPanel(16)

        self.motor_lb.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder,0,0)
        self.motor_rb.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.motor_rb.selectProfileSlot(0, 0)
        self.motor_lb.selectProfileSlot(0, 0)
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
        self.computed_velocity = 0


        self.logger = None

    def dumb_turn(self):
        self.drive.arcadeDrive(0, 0.4, False)

    def execute_turn(self, angle):
        position = angle / 60.
        self.motor_rb.set(ctre._impl.ControlMode.MotionMagic, self.ratio * position)
        self.motor_lb.set(ctre._impl.ControlMode.MotionMagic, self.ratio * position)
        self.drive.feed()

    def initDefaultCommand(self):
        self.setDefaultCommand(Drive())

    def init_logger(self):
        self.logger = DataLogger('drivetrain.csv')
        self.logger.add("time", lambda: self.timer.get())
        self.logger.add("heading", lambda: self.navx.getAngle())
        self.logger.add("enc_pos_l", lambda: self.motor_lb.getSelectedSensorPosition(0))
        self.logger.add("enc_pos_r", lambda: self.motor_rb.getSelectedSensorPosition(0))
        self.logger.add("enc_vel_l", lambda: self.motor_lb.getSelectedSensorVelocity(0))
        self.logger.add("enc_vel_r", lambda: self.motor_rb.getSelectedSensorVelocity(0))
        self.logger.add("error_l", lambda: self.motor_lb.getClosedLoopError(0))
        self.logger.add("error_r", lambda: self.motor_rb.getClosedLoopError(0))
        self.logger.add("target_l", lambda: self.motor_lb.getClosedLoopTarget(0))
        self.logger.add("target_r", lambda: self.motor_rb.getClosedLoopTarget(0))
        self.logger.add("computed_velocity", lambda: self.computed_velocity)
        self.logger.add("mode", lambda: self.mode)
        self.logger.add("voltage", lambda: self.motor_lb.getBusVoltage())
        self.logger.add("voltagep_l", lambda: self.motor_lb.getMotorOutputPercent())
        self.logger.add("voltagep_r", lambda: self.motor_rb.getMotorOutputPercent())
        self.logger.add("current_rf", lambda: self.pdp.getCurrent(0))
        self.logger.add("current_rb", lambda: self.pdp.getCurrent(1))
        self.logger.add("current_lf", lambda: self.pdp.getCurrent(15))
        self.logger.add("current_lb", lambda: self.pdp.getCurrent(13))

    def zeroEncoders(self):
        self.motor_rb.setSelectedSensorPosition(0, 0, 0)
        self.motor_lb.setSelectedSensorPosition(0, 0, 0)

    def zeroNavx(self):
        self.navx.reset()

    def initialize_driveTurnlike(self):
        #The PID values with the motors
        self.zeroEncoders()
        self.motor_rb.configMotionAcceleration(int(self.getEncoderAccel(1.25)), 0)
        self.motor_lb.configMotionAcceleration(int(self.getEncoderAccel(1.25)), 0)
        self.motor_rb.configMotionCruiseVelocity(int(self.getEncoderVelocity(2.5)), 0)
        self.motor_lb.configMotionCruiseVelocity(int(self.getEncoderVelocity(2.5)), 0)
        self.motor_rb.configNominalOutputForward(.1, 0)
        self.motor_lb.configNominalOutputForward(.1, 0)
        self.motor_rb.configNominalOutputReverse(-0.1, 0)
        self.motor_lb.configNominalOutputReverse(-0.1, 0)
        self.motor_rb.configPeakOutputForward(0.4, 0)
        self.motor_lb.configPeakOutputForward(0.4, 0)
        self.motor_rb.configPeakOutputReverse(-0.4, 0)
        self.motor_lb.configPeakOutputReverse(-0.4, 0)
        self.motor_rb.selectProfileSlot(0, 0)
        self.motor_lb.selectProfileSlot(0, 0)
        # self.motor_rb.config_kF(0, 0, 0)
        # self.motor_lb.config_kF(0, 0, 0)
        self.motor_rb.config_kP(0, 0.18, 0)
        self.motor_lb.config_kP(0, 0.18, 0)
        self.motor_rb.config_kI(0, 0, 0)
        self.motor_lb.config_kI(0, 0, 0)
        self.motor_rb.config_kD(0, 8, 0)
        self.motor_lb.config_kD(0, 8, 0)

    def uninitialize_driveTurnlike(self):
        #The PID values with the motors
        self.motor_rb.configNominalOutputForward(0, 0)
        self.motor_lb.configNominalOutputForward(0, 0)
        self.motor_rb.configNominalOutputReverse(0, 0)
        self.motor_lb.configNominalOutputReverse(0, 0)
        self.motor_rb.configPeakOutputForward(1, 0)
        self.motor_lb.configPeakOutputForward(1, 0)
        self.motor_rb.configPeakOutputReverse(-1, 0)
        self.motor_lb.configPeakOutputReverse(-1, 0)

    def initilize_driveForward(self):
        self.mode = "Forward"
        #The PID values with the motors for drive forward
        self.zeroEncoders()
        self.motor_rb.configMotionAcceleration(int(self.getEncoderAccel(5)), 0)
        self.motor_lb.configMotionAcceleration(int(self.getEncoderAccel(5)), 0)
        self.motor_rb.configMotionCruiseVelocity(int(self.getEncoderVelocity(5)), 0)
        self.motor_lb.configMotionCruiseVelocity(int(self.getEncoderVelocity(5)), 0)
        self.motor_rb.configNominalOutputForward(0, 0)
        self.motor_lb.configNominalOutputForward(0, 0)
        self.motor_rb.configNominalOutputReverse(0, 0)
        self.motor_lb.configNominalOutputReverse(0, 0)
        self.motor_rb.configPeakOutputForward(1, 0)
        self.motor_lb.configPeakOutputForward(1, 0)
        self.motor_rb.configPeakOutputReverse(-1, 0)
        self.motor_lb.configPeakOutputReverse(-1, 0)
        self.motor_rb.selectProfileSlot(0, 0)
        self.motor_lb.selectProfileSlot(0, 0)
        self.motor_rb.config_kF(0, 0, 0)
        self.motor_lb.config_kF(0, 0, 0)
        self.motor_rb.config_kP(0, 0.18, 0)
        self.motor_lb.config_kP(0, 0.18, 0)
        self.motor_rb.config_kI(0, 0, 0)
        self.motor_lb.config_kI(0, 0, 0)
        self.motor_rb.config_kD(0, 2, 0)
        self.motor_lb.config_kD(0, 2, 0)

    def initialize_velocity_closedloop(self):
        self.motor_rb.configNominalOutputForward(0, 0)
        self.motor_lb.configNominalOutputForward(0, 0)
        self.motor_rb.configNominalOutputReverse(0, 0)
        self.motor_lb.configNominalOutputReverse(0, 0)
        self.motor_rb.configPeakOutputForward(1, 0)
        self.motor_lb.configPeakOutputForward(1, 0)
        self.motor_rb.configPeakOutputReverse(-1, 0)
        self.motor_lb.configPeakOutputReverse(-1, 0)
        self.motor_rb.selectProfileSlot(0, 0)
        self.motor_lb.selectProfileSlot(0, 0)
        # tested for counterclockwise turn

        self.motor_rb.config_kF(0, 1.88, 0)
        self.motor_rb.config_kP(0, 4.18, 0)
        self.motor_rb.config_kI(0, 0.01, 0)
        self.motor_rb.config_kD(0, 450, 0)

        self.motor_lb.config_kF(0, 0.88, 0)
        self.motor_lb.config_kP(0, 3.18, 0)
        self.motor_lb.config_kI(0, 0.01, 0)
        self.motor_lb.config_kD(0, 450, 0)

    def getAngle(self):
        return self.navx.getAngle()

    def set_turn_velocity(self, v_degps):
        velocity_ratio = 1.6
        self.computed_velocity = v_encp100ms = velocity_ratio * v_degps
        #self.computed_velocity = v_encp100ms = 32
        self.motor_rb.set(ctre.ControlMode.Velocity, v_encp100ms)
        self.motor_lb.set(ctre.ControlMode.Velocity, v_encp100ms)

    def execute_driveforward(self, positionL, positionR):
        self.motor_rb.set(ctre._impl.ControlMode.MotionMagic, self.ratio * positionR)
        self.motor_lb.set(ctre._impl.ControlMode.MotionMagic, self.ratio * positionL)
        self.drive.feed()

    def isFinished_driveforward(self, target):
        sensorPL = self.motor_lb.getSelectedSensorPosition(0)
        a1 = (target-0.2)*self.ratio
        a2 = (target+0.2)*self.ratio
        if a1 < sensorPL < a2:
            return True


    def end_driveforward(self):
        self.motor_rb.set(0)
        self.motor_lb.set(0)
        self.mode = ""

    off = end_driveforward

    def getEncoderVelocity(self, fps):
        return fps*self.ratio/10

    def getEncoderAccel(self, fps2):
        return fps2*self.ratio/10




    def periodic(self):
        #Variables for the Navx
        angle = self.navx.getAngle()
        self.navx_table.putNumber('Angle', angle)


        #Variables used for the dashboard
        sensorPL = self.motor_lb.getSelectedSensorPosition(0)
        self.leftEncoder_table.putNumber("Position", sensorPL)

        sensorPR = self.motor_rb.getSelectedSensorPosition(0)
        self.rightEncoder_table.putNumber("Position", sensorPR)

        sensorVL = self.motor_lb.getSelectedSensorVelocity(0)
        self.leftEncoder_table.putNumber("Velocity", sensorVL)

        sensorVR = self.motor_rb.getSelectedSensorVelocity(0)
        self.rightEncoder_table.putNumber("Velocity", sensorVR)

        voltageL = self.motor_lb.getMotorOutputPercent()
        voltageR = self.motor_rb.getMotorOutputPercent()

        self.leftError.putNumber("Voltage", voltageL)
        self.rightError.putNumber("Voltage", voltageR)

        if self.logger is not None:
            self.logger.log()
