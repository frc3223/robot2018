#!/usr/bin/env python3

import wpilib
from robotpy_ext.common_drivers import navx

class Gneiss(wpilib.IterativeRobot):
    '''Main robot class'''
    
    def robotInit(self):
        '''Robot-wide initialization code should go here'''
        self.joystick = wpilib.Joystick(0)
        self.motor_rr = wpilib.Victor(2)
        self.motor_lr = wpilib.Victor(1)
        self.motors = [self.motor_rr, self.motor_lr]
        self.drive = wpilib.RobotDrive(self.motor_lr, self.motor_rr)
        self.navx = navx.AHRS.create_spi()
        self.gyro = wpilib.AnalogGyro(1)
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

