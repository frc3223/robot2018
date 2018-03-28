import wpilib.command
from profiler import TrapezoidalProfile


class TurnProfiledRight(wpilib.command.Command):
    """
    velocity closed loop inside the talon,
    in here, listen to gyro and build a motion profile to drive velocity
    """
    def __init__(self, angle):
        super().__init__("TurnProfiled")
        self.drivetrain = self.getRobot().drivetrain
        self.requires(self.drivetrain)
        # degrees
        self.profiler = TrapezoidalProfile(cruise_v=70, a=50, target_pos=angle, tolerance=5)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.drivetrain.zeroNavx()
        self.drivetrain.initialize_velocity_closedloop()
        self.timer.start()

    def execute(self):
        dt = self.timer.get()
        self.timer.reset()
        pos = self.drivetrain.getAngle()
        self.profiler.calculate_new_velocity(pos, dt)
        self.drivetrain.set_turn_velocity(self.profiler.current_target_v)

    def isFinished(self):
        return False

    def end(self):
        self.drivetrain.off()
        self.timer.stop()
