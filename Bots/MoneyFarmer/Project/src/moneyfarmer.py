import pyautogui
from botStateMachine import *
from threading import Thread, Lock
from time import sleep

class MoneyFarmer(BotStateMachine):

    windowCapture = None
    detection = None
    running = False
    lock = None

    def __init__(self, windowCapture, detection):
        super().__init__()
        self.lock = Lock()
        self.windowCapture = windowCapture
        self.detection = detection
    
    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()
        
    def run(self):
        self.setState(Init(self))
        while(self.running):
            self.runState()
            
    def stop(self):
        self.running = False

    def setState(self, state):
        super().setState(state)
        self.lock.acquire()
        self.detection.setState(state)
        self.lock.release()

class Init(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self):
        pyautogui.press('x')
    
    def run(self):
        if(not self.bot.detection.checkPixel(22, 51, '0,255,255')):
            self.bot.setState(WaitingScreen(self.bot))

    def exit(self): pass

class WaitingScreen(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pass
    def run(self):
        if(self.bot.detection.checkPixel(22, 51, '0,255,255')):
            self.bot.setState(RunForward(self.bot))
        sleep(0.5)
        
    def exit(self): pass

class RunForward(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pyautogui.keyDown('w')
    def run(self):
        if(not self.bot.detection.checkPixel(98, 98, '180,173,238')):
            pyautogui.keyUp('w')
            self.bot.setState(Fight(self.bot))
        sleep(0.5)
    def exit(self): pass

class Fight(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): print('Entering fight')
    def run(self): pass
    def exit(self): pass