from botstatemachine import *
from init import *
from windowcapture import WindowCapture
from wincaputil import *
from time import sleep
import cv2 as cv

class MoneyFarmer(BotStateMachine):
    def __init__(self, windowHandle):
        super().__init__()
        self.windowHandle = windowHandle
        self.screenshot = None

    def setScreenShot(self, screenshot):
        self.screenshot = screenshot

if(__name__ == '__main__'):
    try:
        # Get window handle for specified window
        windowName = 'Wizard101'
        windowHandle = getWindowHandle(windowName)

        # Pass windowhandle to statemachine so states can access it and set initial state
        bot = MoneyFarmer(windowHandle)
        bot.setState(Init(bot))

        while(True):
            try:
                # Check if window is minimized or maximized, if yes throw an exception
                checkWindowFormat(windowHandle)

                # Get screenshot
                windowCapture = WindowCapture(windowHandle)
                screenshot = windowCapture.get_screenshot()
                #cv.imshow(windowName + 'Feed', screenshot)

                # Pass Screenshot to statemachine and run current state
                bot.setScreenShot(screenshot)
                bot.run()

                # Listen for exit key
                if cv.waitKey(1) == ord('q'):
                    cv.destroyAllWindows()
                    break

            #Window is either minimized or maximized
            except IncorrectWindowFormatException as e:
                print(e)
                sleep(2)

    #Window with specified name not found
    except WindowNotFoundException as e:
        print(e)

    #Window has been closed
    except WindowClosedException as e:
        print(e)

    except Exception as e:
        print('An Error has occured: ' + e)

    print('Terminating.')