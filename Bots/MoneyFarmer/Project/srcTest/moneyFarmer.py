import pyautogui
from botStateMachine import *
from threading import Thread
from time import sleep

class MoneyFarmer(BotStateMachine):

    windowCapture = None
    running = False

    def __init__(self, windowCapture):
        super().__init__()
        self.windowCapture = windowCapture
    
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

class Init(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self):
        pyautogui.press('x')
    
    def run(self):
        controlPixelX, controlPixelY = (22, 51)
        controlPixelColorString = '0,255,255'

        screenshot = self.bot.windowCapture.screenshot
        pixelColorString = getPixelColorString(controlPixelX, controlPixelY, screenshot)
        if(pixelColorString != controlPixelColorString):
            self.bot.setState(WaitingScreen(self.bot))

    def exit(self): pass

class WaitingScreen(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pass
    def run(self):
        controlPixelX, controlPixelY = (22, 51)
        controlPixelColorString = '0,255,255'

        screenshot = self.bot.windowCapture.screenshot
        pixelColorString = getPixelColorString(controlPixelX, controlPixelY, screenshot)
        if(pixelColorString == controlPixelColorString):
            pyautogui.keyUp('w')
            self.bot.setState(RunForward(self.bot))
        sleep(0.5)
    def exit(self): pass

class RunForward(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pyautogui.keyDown('w')
    def run(self):
        controlPixelX, controlPixelY = (98,98)
        controlPixelColorString = '180,173,238'

        screenshot = self.bot.windowCapture.screenshot
        pixelColorString = getPixelColorString(controlPixelX, controlPixelY, screenshot)
        if(pixelColorString != controlPixelColorString):
            pyautogui.keyUp('w')
            self.bot.setState(Fight(self.bot))
        sleep(0.5)
    def exit(self): pass

class Fight(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): print('Fight entered')
    def run(self): pass
    def exit(self): pass

def getPixelColorString(x, y, screenshot):
    pixelColor = screenshot[y][x]
    r, g, b = pixelColor
    pixelColorString = str(r) + ',' + str(g) + "," + str(b)
    return pixelColorString

