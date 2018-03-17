import ctre
import networktables
import wpilib

from wpilib.command.subsystem import Subsystem
from commands.elevator_test import ElevatorTest
from data_logger import DataLogger


class Elevator(Subsystem):
    #: encoder ticks per revolution (need ticks per ft)
    ratio = 4096
    max_pos = 3
    min_pos = 0

    def __init__(self):
        super().__init__('Elevator')

        self.sensor = wpilib.DigitalInput(9) # temp num, true is on
        self.motor = ctre.WPI_TalonSRX(3)
        self.other_motor = ctre.WPI_TalonSRX(2)
        self.other_motor.follow(self.motor)
        self.zeroed = False
        self.motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.motor.configOpenLoopRamp(0, 0)
        self.elevator_table = networktables.NetworkTables.getTable('/Elevator')
        self.motor.setSensorPhase(True)
        self.initialize_motionMagic()
        self.fan = wpilib.PWM(1)
        self.timer = wpilib.Timer()
        self.timer.start()
        self.logger = None
        self.init_logger()


    def init_logger(self):
        self.logger = DataLogger('elevator.csv')
        self.logger.add("time", lambda: self.timer.get())
        self.logger.add("enc_pos", lambda: self.motor.getSelectedSensorPosition(0))
        #self.logger.add("voltagep_motor", lambda: self.motor.getMotorOutputPercent())
        #self.logger.add("voltagep_othermotor", lambda: self.other_motor.getMotorOutputPercent())
        self.logger.add("voltage", lambda: self.motor.getBusVoltage())
        self.logger.add("current_motor", lambda: self.motor.getOutputCurrent())
        self.logger.add("current_othermotor", lambda: self.other_motor.getOutputCurrent())
        self.logger.add("zeroed", lambda: 1 if self.zeroed else 0)

    def initialize_motionMagic(self):
        self.motor.configMotionAcceleration(int(self.ftToEncoder_accel(1)), 0)
        self.motor.configMotionCruiseVelocity(int(self.ftToEncoder_vel(1)), 0)
        self.motor.configNominalOutputForward(0, 0)
        self.motor.configNominalOutputReverse(0, 0)
        self.motor.configPeakOutputForward(1.0, 0)
        self.motor.configPeakOutputReverse(-0.8, 0)
        self.motor.selectProfileSlot(0, 0)
        self.motor.config_kF(0, 0, 0)
        self.motor.config_kP(0, 0.018, 0)
        self.motor.config_kI(0, 0, 0)
        self.motor.config_kD(0, 0, 0)

    def set_position(self, position):
        raise Exception("zeroing, limits, and pid have not been configured yet")
        if(position > self.max_pos):
            position = self.max_pos
        if(position < self.min_pos):
            position = self.min_pos
        self.motor.set(ctre.ControlMode.MotionMagic, position * self.ratio)

    def initDefaultCommand(self):
        self.setDefaultCommand(ElevatorTest())

    def ftToEncoder_accel(self, ftPerSec_sq):
        return ftPerSec_sq * self.ratio/10

    def ftToEncoder_vel(self, ftPerSec):
        return ftPerSec * self.ratio/10

    def hover(self):
        self.motor.set(0.1)
        self.fan.setSpeed(1.0)

    def descend(self, voltage):
        pass

    def ascend(self, voltage):
        self.motor.set(voltage)

    def test_drive_x(self, x):
        self.motor.set(x)

    def test_drive_positive(self):
        self.motor.set(0.8)

    def test_drive_negative(self):
        self.motor.set(-0.6)

    def off(self):
        self.motor.stopMotor()

    def zeroEncoder(self):
        self.zeroed = True
        self.motor.setSelectedSensorPosition(0, 0, 0)

    def getEncoderPosition(self):
        return -self.motor.getSelectedSensorPosition(0)


    def getSensor(self):
        return self.sensor.get()

    def periodic(self):
        position = self.motor.getSelectedSensorPosition(0)
        self.elevator_table.putNumber("Position", position)
        self.elevator_table.putNumber("Motor Current", self.motor.getOutputCurrent())
        self.elevator_table.putNumber("Other Motor Current", self.other_motor.getOutputCurrent())
        self.elevator_table.putBoolean("Zeroed", self.zeroed)

        if self.logger is not None:
            self.logger.log()
