#!/usr/bin/env python3

import wpilib
from robotpy_ext.common_drivers import navx
import ctre
import wpilib.drive
from .oi import getJoystick
from .subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from .commands.drive import Drive



class Gneiss(wpilib.IterativeRobot):
    '''Main robot class'''
    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        Command.getRobot = lambda: self

        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.intake = Intake()


        self.joystick = getJoystick()

        self.drivecommand = Drive()



    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        self.drivecommand.cancel()

    def autonomousPeriodic(self):
        '''Called every 20ms in autonomous mode'''
        pass

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        self.drivecommand.cancel()
    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        self.drivecommand.start()

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        pass
        

if __name__ == '__main__':
    wpilib.run(Gneiss)

