from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

joystick = None

def getJoystick():
    global joystick
    if(joystick is None):
        joystick = Joystick(0)
        trigger = JoystickButton(joystick, Joystick.ButtonType.kTrigger)
    return joystick