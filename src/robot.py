#!/usr/bin/env python3
#Imports for the code that adds the needed libraries
import wpilib
from robotpy_ext.common_drivers import navx
import ctre
import wpilib.drive
from commandbased import CommandBasedRobot
from commands import turntoangle
from wpilib.buttons.joystickbutton import JoystickButton

from oi import getJoystick
from subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from commands.drive import Drive
import networktables
from commands import driveForward
from commands import turnlikeistuesday

class Gneiss(CommandBasedRobot):
    '''Main robot class'''
    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        Command.getRobot = lambda x=0: self
        #Variables that are used by the code
        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.intake = Intake()
        self.table = networktables.NetworkTables.getTable("String")
        self.joystick = getJoystick()
        self.angle = turnlikeistuesday.Turnlikeistuesday(1.64)
        self.DriveForward = driveForward.DriveForward()

    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
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

    def teleopPeriodic(self):
        super().teleopPeriodic()
        for i in range(1,11):
            button = self.joystick.getRawButton(i)
            self.table.putBoolean("button"+str(i), button)

        for i in range(0,7):
            axis = self.joystick.getRawAxis(i)
            self.table.putNumber("Axis"+str(i),axis)

        #joystick = wpilib.Joystick(8)
        #joystick.getPOV()
        for i in range(1):
            pov = self.joystick.getPOV(0)
            self.table.putNumber("POV"+str(i),pov)


if __name__ == '__main__':
    wpilib.run(Gneiss)

