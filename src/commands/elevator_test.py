from wpilib.command import Command

from data_logger import DataLogger
from oi import getJoystick

import wpilib

class ElevatorTest(Command):
    def __init__(self):
        super().__init__('ElevatorTest')
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)
        self.joystick = getJoystick()


    def execute(self):
        isDisabled = wpilib.DriverStation.getInstance().isDisabled()
        if self.joystick.getPOV(0) == 0: #Up on D-pad pressed
            self.elevator.test_drive_positive()
        elif self.joystick.getPOV(0) == 180: #Down on D-pad pressed
            self.elevator.test_drive_negative()
        elif isDisabled:
            self.elevator.off()
        else:
            self.elevator.hover()


class ElevatorTest2(Command):
    def __init__(self):
        super().__init__("laksdjfkl")
        self.elevator = self.getRobot().elevator
        self.requires(self.elevator)
        self.timer = wpilib.Timer()
        self.done = False
        self.state = 1
        self.voltage = 0.75

    def initialize(self):
        self.logger = DataLogger('elevator-majig.csv')
        self.logger.add("time", lambda: self.timer.get())
        self.logger.add("enc_pos1", lambda: self.elevator.motor.getSelectedSensorVelocity(0))
        self.logger.add("current_motor1", lambda: self.elevator.motor.getOutputCurrent())
        self.logger.add("current_follow1", lambda: self.elevator.other_motor.getOutputCurrent())
        self.logger.add("voltage_motor1", lambda: self.elevator.motor.getMotorOutputVoltage())
        self.logger.add("voltage_follow1", lambda: self.elevator.other_motor.getMotorOutputVoltage())
        self.logger.add("bvoltage_motor1", lambda: self.elevator.motor.getBusVoltage())
        self.logger.add("bvoltage_follow1", lambda: self.elevator.other_motor.getBusVoltage())
        self.logger.add("enc_pos2", lambda: self.elevator.other_right_motor.getSelectedSensorVelocity(0))
        self.logger.add("current_motor2", lambda: self.elevator.right_motor.getOutputCurrent())
        self.logger.add("current_follow2", lambda: self.elevator.other_right_motor.getOutputCurrent())
        self.logger.add("voltage_motor2", lambda: self.elevator.right_motor.getMotorOutputVoltage())
        self.logger.add("voltage_follow2", lambda: self.elevator.other_right_motor.getMotorOutputVoltage())
        self.logger.add("bvoltage_motor2", lambda: self.elevator.right_motor.getBusVoltage())
        self.logger.add("bvoltage_follow2", lambda: self.elevator.other_right_motor.getBusVoltage())

        self.timer.start()



    def execute(self):
        e = self.elevator.getEncoderPosition()
        if self.state == 1:
            self.elevator.ascend(self.voltage)
            if e > 28000:
                self.state = 2
                self.elevator.descend(self.voltage)
        if self.state == 2:
            self.elevator.descend(self.voltage)
        if e < 1000 and self.state == 2:
            self.state = 1
            self.voltage += 0.25
        elif self.voltage > 1:
            self.voltage = 0
            self.done = True




        self.logger.log()

    def isFinished(self):
        return self.done

    def end(self):
        self.elevator.hover()
        self.logger.close()






