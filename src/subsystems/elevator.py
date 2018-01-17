import wpilib

from wpilib.command.subsystem import Subsystem


class Elevator(Subsystem):

    def __init__ (self):

        super().__init__('Elevator')

