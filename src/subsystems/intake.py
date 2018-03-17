import wpilib

import networktables
from wpilib.command.subsystem import Subsystem
from commands import grabber
from data_logger import DataLogger


class Intake(Subsystem):

    def __init__(self):
        super().__init__('Intake')
        self.intake_motor_closeOpen = wpilib.VictorSP(8)
        self.intake_motor_rightWheel = wpilib.VictorSP(9)
        self.intake_motor_leftWheel = wpilib.VictorSP(7)
        self.limit_switch = wpilib.DigitalOutput(0)
        self.pdp = wpilib.PowerDistributionPanel(16)
        self.intake_table = networktables.NetworkTables.getTable('/Intake')

        self.timer = wpilib.Timer()
        self.timer.start()
        self.logger = None

        self.init_logger()

    def initDefaultCommand(self):
        self.setDefaultCommand(grabber.Grabber())

    def closeGrabber(self, x):
        self.motor_closeOpen_set(x)

    def init_logger(self):
        self.logger = DataLogger('intake.csv')
        self.logger.add("time", lambda: self.timer.get())
        self.logger.add("voltagep_r", lambda: self.intake_motor_rightWheel.get())
        self.logger.add("voltagep_m", lambda: self.intake_motor_closeOpen.get())
        self.logger.add("voltagep_l", lambda: self.intake_motor_leftWheel.get())
        self.logger.add("voltage", lambda: self.pdp.getVoltage())
        self.logger.add("current_r", lambda: self.pdp.getCurrent(0))
        self.logger.add("current_m", lambda: self.pdp.getCurrent(1))
        self.logger.add("current_l", lambda: self.pdp.getCurrent(15))

    def openGrabber(self):
        '''
        if self.limit_switch == True:
            self.grabberOff()
        else:'''
        self.motor_closeOpen_set(-0.5)

    def open2Grabber(self):
        self.intake_motor_closeOpen.set(-0.1)
        self.cubeOut()



    def grabberOff(self):
        self.motor_closeOpen_set(0)

    def cubeOut(self):
        self.intake_motor_rightWheel.set(0.5)
        self.intake_motor_leftWheel.set(-0.5)

    def cubeIn(self):
        self.intake_motor_rightWheel.set(-1)
        self.intake_motor_leftWheel.set(1)

    def intakeWheelsOff(self):
        self.intake_motor_rightWheel.set(0)
        self.intake_motor_leftWheel.set(0)

    def motor_closeOpen_set(self, voltage_percent):
        self.intake_motor_closeOpen.set(voltage_percent)

    def motor_rightWheel_set(self, voltage_percent):
        self.intake_motor_rightWheel.set(voltage_percent)

    def motor_leftWheel_set(self, voltage_percent):
        self.intake_motor_leftWheel.set(voltage_percent)

    def periodic(self):
        self.intake_table.putBoolean("LimitSwitch", self.limit_switch.get())

        if self.logger is not None:
            self.logger.log()
