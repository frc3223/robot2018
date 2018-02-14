#!/usr/bin/env python3
#Imports for the code that adds the needed libraries
import wpilib
from robotpy_ext.common_drivers import navx
import ctre
import wpilib.drive
from commandbased import CommandBasedRobot
from commands import turntoangle, turn_profiled
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons.trigger import Trigger

from oi import getJoystick
from subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from commands.drive import Drive
import networktables
from commands import driveForward
from commands import turnlikeistuesday
import commands
from wpilib.command import scheduler

class Gneiss(CommandBasedRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        Command.getRobot = lambda x=0: self
        #Variables that are used by the code
        self.gamecode = wpilib.DriverStation.getGameSpecificMessage()
        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.intake = Intake()
        self.table = networktables.NetworkTables.getTable("String")
        self.joystick = getJoystick()
        #self.angle = turnlikeistuesday.Turnlikeistuesday(90)
        self.angle = turn_profiled.TurnProfiled(90)
        self.DriveForward = driveForward.DriveForward()
        '''
        self.goToPickup = commands.elevatorPickupHeight()
        self.goToScale = commands.elevatorScaleHeight()
        self.goToSwitch = commands.elevatorSwitchHeight()
        self.goDown = commands.elevatorDownHeight()
        self.pullIn = commands.grabberPullIn()
        self.spitOut = commands.grabberSpitOut()
        '''


    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        self.elevator.setSolenoidState(true) #assumes true is open

        pass

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        #How the buttons for the xbox controller are mapped
        self.drivetrain.init_logger()
        b = JoystickButton(self.joystick, 1) #A
        b2 = JoystickButton(self.joystick, 2) #B
        b.whenPressed(self.angle)
        b2.cancelWhenPressed(self.angle)

        b3 = JoystickButton(self.joystick, 3) #X
        b4 = JoystickButton(self.joystick, 4) #Y
        b3.whenPressed(self.DriveForward)
        b4.cancelWhenPressed(self.DriveForward)

        '''
        pickupheight_button = JoystickButton(self.joystick, 1) #A
        pickupheight_button.whenPressed(self.goToPickup)
        switchheight_button = JoystickButton(self.joystick, 2)#B
        switchheight_button.whenPressed(self.goToSwitch)
        elevatordown_button = JoystickButton(self.joystick, 3) #X
        elevatordown_button.whenPressed(self.goDown)
        scaleheight_button = JoystickButton(self.joystick, 4) #Y
        scaleheight_button.whenPressed(self.goToScale)
        spitout_button = JoystickButton(self.joystick, 6) #Right Bumper
        spitout_button.whenPressed(self.spitOut)
        pullin_button = JoystickButton(self.joystick, 5) #Left Bumper
        pullin_button.whenPressed(self.pullIn)
        '''


if __name__ == '__main__':
    wpilib.run(Gneiss)
