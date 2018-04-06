from wpilib.command import Command, InstantCommand

class MultiConditionalCommand(Command):
    
    def __init__(self, name, commands):
        super().__init__(name)

        self.commands = commands

        self.chosenCommand = None
        
        self.requireAll()

    def requireAll(self):
        for condition_name, command in self.commands:
            assert hasattr(self, condition_name), 'unspecified condition: %s' % condition_name
            for e in command.getRequirements():
                self.requires(e)
            
    def _initialize(self):
        '''
            Calls conditions, and runs the proper command.
        '''
        for condition_name, command in self.commands:
            condition = getattr(self, condition_name)()
            if condition:
                self.chosenCommand = command
                break
            
        if self.chosenCommand is not None:
            # This is a hack to make cancelling the chosen command inside a CommandGroup work properly
            self.chosenCommand.clearRequirements()
        
            self.chosenCommand.start()
        
        super()._initialize()
    
    def _cancel(self):
        if self.chosenCommand is not None and self.chosenCommand.isRunning():
            self.chosenCommand.cancel()
            
        super()._cancel()
    
    def isFinished(self):
        if self.chosenCommand is not None:
            return self.chosenCommand.isCompleted()
        else:
            return True
    
    def _interrupted(self):
        if self.chosenCommand is not None and self.chosenCommand.isRunning():
            self.chosenCommand.cancel()
            
        super()._interrupted()
