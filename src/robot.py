#!/usr/bin/env python3
import wpilib
import ctre
import wpilib.drive
import networktables
import commands
from robotpy_ext.common_drivers import navx
from commandbased import CommandBasedRobot
from commands import turn_profiled
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons.trigger import Trigger

from oi import getJoystick
from subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from commands.drive import Drive
from commands import (
    driveForward,
    turnlikeistuesday,
    automous,
    autoTimeBased,
    autoEncoders)
from wpilib.command import scheduler

class Gneiss(CommandBasedRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

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
        #self.angle = turnlikeistuesday.Turnlikeistuesday(90)
        self.angle = turn_profiled.TurnProfiled(90)
        self.auto = driveForward.DriveForward(10)
        #self.autoTimeBased = autoTimeBased.TimeBasedStart()
        self.autoEncoders = commands.autoEncoders.AutoEncodersTurnLeft(90)
        '''self.elevatorZero = elevatorZero.elevatorZero()'''

        self.driveForward = driveForward.DriveForward(10)
        #self.driveForward = automous.Test()

    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        '''if self.startSide == "l":
            if self.gamecode[1:] == "l": #L the Letter
                gotoSwitchL.gotoSwitchL("l").start()
            else: if self.gamecode[:2][1:] == "l":
                goToScaleL.goToScaleL("l").start()
            else:
                goToSwitchL.gotoSwitchL("r").start()'''
        self.autoEncoders.start()

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        self.drivetrain.zeroEncoders()
        #How the buttons for the xbox controller are mapped
        self.drivetrain.init_logger()
        b = JoystickButton(self.joystick, 7) #A
        b2 = JoystickButton(self.joystick, 8) #B
        #b.whenPressed(self.angle)
        b2.cancelWhenPressed(self.angle)

        #b3 = JoystickButton(self.joystick, 3) #X
        #b4 = JoystickButton(self.joystick, 4) #Y
        #b3.whenPressed(self.driveForward)
        #b4.cancelWhenPressed(self.driveForward)

        #b5 = JoystickButton(self.joystick, 5) #leftbumper
        #b6 = JoystickButton(self.joystick, 6) #rightbumper
        #b5.whenPressed(self.auto)
        #b6.cancelWhenPressed(self.auto)

if __name__ == '__main__':
    wpilib.run(Gneiss)
