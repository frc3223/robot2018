import wpilib.command
import ctre


class DriveForward(wpilib.command.Command):
    ratio = 888

    def __init__(self):
        super().__init__("DriveForward")
        self.requires(self.getRobot().drivetrain)
        self.drivetrain = self.getRobot().drivetrain
        self.drivetrain.motor_lb.setInverted(True)

    def initialize(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.motor_rb.configMotionAcceleration(int(self.drivetrain.getEncoderAccel(5)), 0)
        self.drivetrain.motor_lb.configMotionAcceleration(int(self.drivetrain.getEncoderAccel(5)), 0)
        self.drivetrain.motor_rb.configMotionCruiseVelocity(int(self.drivetrain.getEncoderVelocity(5)), 0)
        self.drivetrain.motor_lb.configMotionCruiseVelocity(int(self.drivetrain.getEncoderVelocity(5)), 0)
        self.drivetrain.motor_rb.configNominalOutputForward(0, 0)
        self.drivetrain.motor_lb.configNominalOutputForward(0, 0)
        self.drivetrain.motor_rb.configNominalOutputReverse(0, 0)
        self.drivetrain.motor_lb.configNominalOutputReverse(0, 0)
        #self.drivetrain.motor_rb.configPeakOutputForward(1, 0)
        #self.drivetrain.motor_lb.configPeakOutputForward(1, 0)
        #self.drivetrain.motor_rb.configPeakOutputReverse(-1, 0)
        #self.drivetrain.motor_lb.configPeakOutputReverse(-1, 0)
        self.drivetrain.motor_rb.selectProfileSlot(0, 0)
        self.drivetrain.motor_lb.selectProfileSlot(0, 0)
        self.drivetrain.motor_rb.config_kF(0,2.3, 0)
        self.drivetrain.motor_lb.config_kF(0, 2.3, 0)
        self.drivetrain.motor_rb.config_kP(0, 0, 0)
        self.drivetrain.motor_lb.config_kP(0, 0, 0)
        self.drivetrain.motor_rb.config_kI(0, 0, 0)
        self.drivetrain.motor_lb.config_kI(0, 0, 0)
        self.drivetrain.motor_rb.config_kD(0, 0, 0)
        self.drivetrain.motor_lb.config_kD(0, 0, 0)


    def execute(self):
        self.drivetrain.drive.arcadeDrive(-0.4,0)
        self.drivetrain.motor_rb.set(ctre._impl.ControlMode.MotionMagic, self.ratio*20)
        self.drivetrain.motor_lb.set(ctre._impl.ControlMode.MotionMagic, self.ratio*20)



    def isFinished(self):
        sensorPL = self.drivetrain.motor_lb.getSelectedSensorPosition(0)
        return sensorPL > 3.5*self.ratio

    def end(self):
        self.drivetrain.motor_rb.set(0)
        self.drivetrain.motor_lb.set(0)
        # doesn't compensate for deceleration




