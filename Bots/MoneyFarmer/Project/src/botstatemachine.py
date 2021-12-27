class BotStateMachine:
    def __init__(self, initState = None):
        self.state = initState

    def setState(self, state):
        if(not self.state == None):
            self.state.exit()
        self.state = state
        state.enter()

    def runState(self):
        self.state.run()

class State:
    def __init__(self, bot):
        self.bot = bot

    def enter(self): pass
    def run(self): pass
    def exit(self): pass