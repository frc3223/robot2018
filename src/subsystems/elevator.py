import wpilib
import ctre

from wpilib.command.subsystem import Subsystem


class Elevator(Subsystem):

    def __init__(self):
        super().__init__('Elevator')
        self.motor2 = ctre.WPI_TalonSRX(3)
        self.motor14 = ctre.WPI_TalonSRX(12)
        self.solenoid = wpilib.Solenoid(5) #temp num, might be doubleSolenoid


    def getSolenoidState(self): #returns solenoid bool
        return self.solenoid.get()

    def setSolenoidState(self, state): #takes bool, sets solenoid
        self.solenoid.set(state)
