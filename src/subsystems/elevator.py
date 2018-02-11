import ctre
import networktables

from wpilib.command.subsystem import Subsystem
from commands.elevator_test import ElevatorTest


class Elevator(Subsystem):
    #: encoder ticks per revolution
    ratio = 4096

    def __init__(self):
        super().__init__('Elevator')
        self.motor = ctre.WPI_TalonSRX(14)
        self.other_motor = ctre.WPI_TalonSRX(2)
        self.other_motor.follow(self.motor)
        self.zeroed = False
        self.motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.QuadEncoder, 0, 0)
        #self.motor.setSensorPhase(True)
        self.elevator_table = networktables.NetworkTables.getTable('/Elevator')

    def initDefaultCommand(self):
        self.setDefaultCommand(ElevatorTest())

    def test_drive_positive(self):
        self.motor.set(0.1)

    def test_drive_negative(self):
        self.motor.set(-0.1)

    def off(self):
        self.motor.stopMotor()

    def zeroEncoder(self):
        self.zeroed = True
        self.motor.setSelectedSensorPosition(0, 0, 0)

    def periodic(self):
        position = self.motor.getSelectedSensorPosition(0)
        self.elevator_table.putNumber("Position", position)
