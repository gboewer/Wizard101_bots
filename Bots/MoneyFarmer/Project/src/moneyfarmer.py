from botstatemachine import *
from wincaputil import IncorrectWindowFormatException
from time import sleep
import cv2 as cv

class MoneyFarmer(BotStateMachine):
    def __init__(self, windowInterface):
        super().__init__()
        self.windowInterface = windowInterface

    def start(self):
        def printRBG(event,x,y,flags,param):
            if event == cv.EVENT_LBUTTONDBLCLK:
                print(str(x) + ',' + str(y) + ': ' + self.windowInterface.getPixelColorString(x,y))

        displayWindowName = 'Window Feed'
        cv.namedWindow(displayWindowName)
        cv.setMouseCallback(displayWindowName, printRBG)

        self.setState(Init(self))
        while(True):
            try:
                self.windowInterface.getScreenshot()
                self.windowInterface.displayScreenshot(displayWindowName)

                if cv.waitKey(1) == ord('q'):
                    cv.destroyAllWindows()
                    break

                self.runState()
            except IncorrectWindowFormatException as e:
                print(e)
                sleep(2)

class Init(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self):
        self.bot.windowInterface.press_key('x')
    
    def run(self):
        controlPixelCoords = (22, 51)
        controlPixelColorString = "255,255,0"

        try:
            if(self.bot.windowInterface.getPixelColorString(controlPixelCoords) != controlPixelColorString):
                self.bot.setState(RunForward(self.bot))
        except IncorrectWindowFormatException as e:
            print(e)
            sleep(2)

    def exit(self): pass
    
class RunForward(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pass
    def run(self):
        self.bot.windowInterface.hold_key('w', 1)
    def exit(self): pass