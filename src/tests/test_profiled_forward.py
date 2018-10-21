from robot import Rockslide
from commands.profiled_forward import ProfiledForward

def test_profiled_forward(Notifier):
    robot = Rockslide()
    robot.robotInit()

    command = ProfiledForward(10)
    command.initialize()
    command.execute()
    command.isFinished()
    command.end()
