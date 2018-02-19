import wpilib

from wpilib.command.subsystem import Subsystem
import ctre
from commands import grabber


class Intake(Subsystem):

    def __init__(self):
        super().__init__('Intake')
        self.intake_motor_closeOpen = wpilib.VictorSP(6) #insert motor/control number, ie one of the low voltage input numbers
        self.intake_motor_rightWheel = wpilib.VictorSP(7) #insert motor/control number, ie one of the low voltage input numbers
        self.intake_motor_leftWheel = wpilib.VictorSP(8) #insert motor/control number, ie one of the low voltage input numbers

    def initDefaultCommand(self):
        self.setDefaultCommand(grabber.Grabber())

    def motor_closeOpen_set(self, voltage_percent):
        self.intake_motor_closeOpen.set(voltage_percent)

    def motor_rightWheel_set(self, voltage_percent):
        self.intake_motor_rightWheel.set(voltage_percent)

    def motor_leftWheel_set(self, voltage_percent):
        self.intake_motor_leftWheel.set(voltage_percent)
