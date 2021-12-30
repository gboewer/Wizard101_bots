from wincaputil import *
from wizAPI import *
from moneyfarmer import MoneyFarmer

if(__name__ == '__main__'):
    try:
        # Get window handle for specified window
        windowInterface = wizAPI()
        windowInterface.register_window()

        # Pass windowhandle to statemachine so states can access it and set initial state
        bot = MoneyFarmer(windowInterface)
        bot.start()

    # Window with specified name not found
    except WindowNotFoundException as e:
        print(e)

    print('Terminating.')