def test_drivetrain_nt(Notifier):
    import networktables
    from robot import Rockslide

    robot = Rockslide()
    robot.robotInit()
    drivetrain = robot.drivetrain

    drivetrain.periodic()

    assert networktables.NetworkTables.getTable("/Drivetrain/Left").getNumber("Position", None) == 0.0
