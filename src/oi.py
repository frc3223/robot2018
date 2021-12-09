from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

joystick = None
joystick1 = None

def getJoystick():
    global joystick
    if joystick is None:
        joystick = Joystick(0)

    return joystick


def getJoystick1():
    global joystick1
    if joystick1 is None:
        joystick1 = Joystick(1)

    return joystick1
