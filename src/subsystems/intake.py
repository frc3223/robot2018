import wpilib

from wpilib.command.subsystem import Subsystem


class Intake(Subsystem):

    def __init__(self):

        super().__init__('Intake')

