from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton



def getJoystick():

    joystick = Joystick(0)

    trigger = JoystickButton(joystick, Joystick.ButtonType.kTrigger)

    return joystick