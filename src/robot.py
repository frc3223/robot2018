#!/usr/bin/env python3

import wpilib
from robotpy_ext.common_drivers import navx
import ctre
import wpilib.drive

class Gneiss(wpilib.IterativeRobot):
    '''Main robot class'''
    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''
        self.joystick = wpilib.Joystick(0)
        self.motor_rb = ctre.WPI_TalonSRX(2)
        self.motor_lb = ctre.WPI_TalonSRX(1)
        self.motor_rf = ctre.WPI_TalonSRX(3)
        self.motor_lf = ctre.WPI_TalonSRX(4)
        self.motors = [self.motor_rb, self.motor_lb, self.motor_rf, self.motor_lf]
        self.drive = wpilib.drive.DifferentialDrive(self.motor_rb, self.motor_lb, self.motor_rf, self.motor_lf)
        self.navx = navx.AHRS.create_spi()

        pass

    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        pass

    def autonomousPeriodic(self):
        '''Called every 20ms in autonomous mode'''
        pass

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        for motor in self.motors:
            motor.set(0)

    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        pass

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        self.drive.arcadeDrive(self.joystick)
        

if __name__ == '__main__':
    wpilib.run(Gneiss)

