import wpilib
import ctre

from wpilib.command.subsystem import Subsystem


class Elevator(Subsystem):

    def __init__(self):
        super().__init__('Elevator')
        self.motor2 = ctre.WPI_TalonSRX(3)
        self.motor14 = ctre.WPI_TalonSRX(12)


