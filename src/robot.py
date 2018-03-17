#!/usr/bin/env python3
import wpilib
import ctre
import wpilib.drive
import networktables
import commands
from robotpy_ext.common_drivers import navx
from commandbased import CommandBasedRobot

from commands.autoEncoders import ElevatorSwitch, ElevatorIntake
from commands import turn_profiledright
from commands import turn_profiledleft
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons.trigger import Trigger

from oi import getJoystick
from subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from commands.drive import Drive
from commands import (
    driveForward,
    turnlikeistuesday,
    autonomous,
    autoTimeBased,
    autoEncoders)
from wpilib.command import scheduler

from commands.autoTimeBased import TimeBasedElevator


class Gneiss(CommandBasedRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        #start camera
        wpilib.CameraServer.launch()

        Command.getRobot = lambda x=0: self
        #Variables that are used by the code
        self.startSide = "l" #starting side
        self.gamecode = "rlr"                 #wpilib.DriverStation.getGameSpecificMessage()
        self.drivetrain = Drivetrain()
        self.drivetrain.zeroEncoders()
        self.elevator = Elevator()
        self.intake = Intake()
        self.table = networktables.NetworkTables.getTable("String")
        self.joystick = getJoystick()
        self.auto = autonomous.SwitchCommands()
        self.elevatorSwitch = ElevatorSwitch()
        self.elevatorIntake = ElevatorIntake()


        self.driveForward = driveForward.DriveForward(10)

    def teleopInit(self):
        buttonA = JoystickButton(self.joystick, 1)
        buttonA.whenPressed(self.elevatorSwitch)
        buttonY = JoystickButton(self.joystick, 4)
        buttonY.cancelWhenPressed(self.elevatorSwitch)
        buttonY.cancelWhenPressed(self.elevatorIntake)

        buttonB = JoystickButton(self.joystick, 2)
        buttonB.whenPressed(self.elevatorIntake)

    def teleopPeriodic(self):
        super().teleopPeriodic()
        self.table.putString("Joystick", self.joystick.getName())

    def autonomousInit(self):
        self.elevator.zeroEncoder()
        self.drivetrain.zeroEncoders()
        '''Called only at the beginning of autonomous mode'''
        '''if self.startSide == "l":
            if self.gamecode[1:] == "l": #L the Letter
                gotoSwitchL.gotoSwitchL("l").start()
            else: if self.gamecode[:2][1:] == "l":
                goToScaleL.goToScaleL("l").start()
            else:
                goToSwitchL.gotoSwitchL("r").start()'''
        self.elevatorSwitch.start()

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass



if __name__ == '__main__':
    wpilib.run(Gneiss)
