from wpilib.command import Command
from commands.multiconditionalcommand import MultiConditionalCommand


def test_multiconditional():

    class MC1(MultiConditionalCommand):
        def condition1(self):
            return False

        def condition2(self):
            return True


    class StubCommand(Command):
        def __init__(self):
            super().__init__()
            self.executed = False
            self.ended = False
            self.beFinished = False
            self.started = False

        def execute(self):
            self.executed = True

        def isFinished(self):
            return self.beFinished

        def end(self):
            self.ended = True

        def start(self):
            self.started = True

    command1 = StubCommand()
    command2 = StubCommand()
    command = MC1("MC1", [
        ("condition1", command1),
        ("condition2", command2),
        ])

    command._initialize()

    command.execute()

    assert not command1.started
    assert command2.started
