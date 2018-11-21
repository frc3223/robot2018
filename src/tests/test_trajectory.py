from commands.trajectories import CsvTrajectoryCommand
from robot import Rockslide


def test_CsvTrajectoryCommand(Notifier):
    robot = Rockslide()
    robot.robotInit()
    command = CsvTrajectoryCommand("traj1.tra")
    command.initialize()
    i = 0
    t = 0
    while not command.isFinished():
        command.execute()
        i += 1
        t += robot.getPeriod()

        assert t < 10

    command.end()
