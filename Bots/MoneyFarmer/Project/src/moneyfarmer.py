from botstatemachine import *
from init import *
from windowcapture import WindowCapture
from wincaputil import *
from time import sleep
from wizAPI import *
import cv2 as cv

class MoneyFarmer(BotStateMachine):
    def __init__(self, windowInterface):
        super().__init__()
        self.windowInterface = windowInterface

    def start(self):
        self.setState(Init(self))
        while(True):
            try:
                # Check window format before running
                self.windowInterface.checkWindowFormat()

                # Run current state
                self.runState()

            except IncorrectWindowFormatException as e:
                print(e)
                sleep(2)

            # Listen for exit key
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break


if(__name__ == '__main__'):
    try:
        # Get window handle for specified window
        windowInterface = wizAPI()
        windowInterface.register_window()

        # Pass windowhandle to statemachine so states can access it and set initial state
        bot = MoneyFarmer(windowInterface)

        # Start bot only when window is neither minimized nor maximized
        while(True):
            try:
                windowInterface.checkWindowFormat()
                bot.start()
                break
            except IncorrectWindowFormatException as e:
                print(e)
                sleep(2)

    # Window with specified name not found
    except WindowNotFoundException as e:
        print(e)

    # Terminate bot if any unforeseen exceptions occur
    except Exception as e:
        print(e)

    print('Terminating.')