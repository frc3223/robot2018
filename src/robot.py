#!/usr/bin/env python3

import wpilib
from robotpy_ext.common_drivers import navx
import ctre
import wpilib.drive
from commandbased import CommandBasedRobot

from oi import getJoystick
from subsystems import (Drivetrain, Elevator, Intake)
from wpilib.command import Command
from commands.drive import Drive


class Gneiss(CommandBasedRobot):
    '''Main robot class'''
    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        Command.getRobot = lambda x=0: self

        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.intake = Intake()

        self.joystick = getJoystick()

    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        pass

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        pass


if __name__ == '__main__':
    wpilib.run(Gneiss)

