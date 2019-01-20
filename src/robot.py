#!/usr/bin/env python3
import wpilib
import wpilib.drive
import networktables
from commandbased import CommandBasedRobot

from commands.autoEncoders import (
    ElevatorSwitch, ElevatorIntake, ElevatorScale, AutoEncoders, AutoEncodersTurnRight
)
from wpilib.buttons.joystickbutton import JoystickButton

from commands.elevator_test import ElevatorTest2
from commands.trajectories import CsvTrajectoryCommand, StateSpaceDriveCommand
from oi import getJoystick
from oi import getJoystick1
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
from commands.profiled_forward import ProfiledForward

class Rockslide(CommandBasedRobot):
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
        self.joystick1 = getJoystick1()
        #self.auto =  driveForward.DriveForward(16)
        #self.auto = AutoEncoders(20)
        #self.auto = ProfiledForward(10)
        self.auto = StateSpaceDriveCommand("straight3m.tra")
        #self.auto = autonomous.Autonomuscc()
        #self.auto = AutoEncoders()
        self.elevatorSwitch = ElevatorSwitch()
        self.elevatorScale = ElevatorScale()
        self.elevatorIntake = ElevatorIntake()


        self.driveForward = driveForward.DriveForward(10)

    def teleopInit(self):
        self.drivetrain.zeroEncoders()
        self.drivetrain.zeroNavx()
        buttonA = JoystickButton(self.joystick1, 1)
        buttonY = JoystickButton(self.joystick1, 4)

        #buttonA.whenPressed(ElevatorTest2())
        buttonA.whenPressed(self.elevatorIntake)
        buttonY.whenPressed(self.elevatorScale)

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
    wpilib.run(Rockslide)
