#!/usr/bin/env python3
import wpilib
import wpilib.drive
import networktables
from commandbased import CommandBasedRobot

from commands.autoEncoders import (
    ElevatorSwitch, ElevatorIntake, ElevatorScale, AutoEncoders, AutoEncodersTurnRight
)
from wpilib.buttons.joystickbutton import JoystickButton

from oi import getJoystick
from subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from commands import (
    driveForward,
    autonomous,
)
from commands.autoEncoders import AutoEncodersTurnRight, AutoEncodersTurnLeft
from commands.turn_profiledright import TurnProfiledRight
from commands.autoNavx import TurnRight, TurnLeft
from commands.autonomous import MiddlePosLeftSwitchAuto, RightPosRightSwitchAuto

class Gneiss(CommandBasedRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        #start camera
        wpilib.CameraServer.launch()

        Command.getRobot = lambda x=0: self
        #Variables that are used by the code
        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.intake = Intake()
        self.table = networktables.NetworkTables.getTable("String")
        self.joystick = getJoystick()
        #self.auto = autonomous.ForwardOnly()
        self.auto = autonomous.SwitchCommands()
        #self.auto = TurnRight(90)
        #self.auto = Wait9ThenForward()
        #self.auto = RightPosRightSwitchAuto()
        #self.auto = AutoEncodersTurnLeft(90)
        #self.auto = MiddlePosLeftSwitchAuto()
        self.elevatorSwitch = ElevatorSwitch()
        self.elevatorScale = ElevatorScale()
        self.elevatorIntake = ElevatorIntake()


        self.driveForward = driveForward.DriveForward(10)

    def teleopInit(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        buttonA = JoystickButton(self.joystick, 1)
        buttonB = JoystickButton(self.joystick, 2)
        buttonY = JoystickButton(self.joystick, 4)

        buttonA.whenPressed(self.elevatorIntake)
        buttonY.whenPressed(self.elevatorScale)
        buttonB.whenPressed(self.elevatorSwitch)

    def teleopPeriodic(self):
        super().teleopPeriodic()
        self.table.putString("Joystick", self.joystick.getName())

    def autonomousInit(self):
        self.elevator.zeroEncoder()
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        self.auto.start()

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass



if __name__ == '__main__':
    wpilib.run(Gneiss)
