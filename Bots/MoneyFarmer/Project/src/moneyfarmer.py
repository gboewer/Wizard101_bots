from botstatemachine import *
from wincaputil import IncorrectWindowFormatException
from time import sleep
import cv2 as cv
import threading
import sys

class MoneyFarmer(BotStateMachine):
    def __init__(self, windowInterface):
        super().__init__()
        self.windowInterface = windowInterface

    def start(self):
        def displayLiveFeed():
            def printRBG(event,x,y,flags,param):
                if event == cv.EVENT_LBUTTONDBLCLK:
                    print(str(x) + ',' + str(y) + ': ' + self.windowInterface.getPixelColorString(x,y))

            while(True):
                try:
                    self.windowInterface.checkWindowFormat()
                    displayWindowName = 'Window Feed'
                    cv.namedWindow(displayWindowName)
                    cv.setMouseCallback(displayWindowName, printRBG)
                    break
                except IncorrectWindowFormatException as e:
                    print(e)
                    sleep(2)

            while(True):
                try:
                    screenshotRGB = self.windowInterface.getScreenshot(False)
                    screenshotBGR = cv.cvtColor(screenshotRGB, cv.COLOR_RGB2BGR)
                    cv.imshow(displayWindowName, screenshotBGR)

                    # Listen for exit key
                    if cv.waitKey(1) == ord('q'):
                        cv.destroyAllWindows()
                        sys.exit()
                except IncorrectWindowFormatException as e:
                    print(e)
                    sleep(2)

        displayThread = threading.Thread(target=displayLiveFeed)
        displayThread.start()

        #self.setState(Init(self))
        #self.runState()

class Init(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self):
        self.bot.windowInterface.press_key('x')
    
    def run(self):
        controlPixelCoords = (22, 51)
        controlPixelColorString = "255,255,0"
        while(True):
            try:
                self.bot.windowInterface.getScreenshot()

                if(self.bot.windowInterface.getPixelColorString(controlPixelCoords) != controlPixelColorString):
                    break
            except IncorrectWindowFormatException as e:
                print(e)
                sleep(2)
        self.bot.setState(RunForward(self.bot))

    def exit(self): pass
    
class RunForward(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pass
    def run(self):
        while(True):
            self.bot.windowInterface.hold_key('w', 1)
    def exit(self): pass