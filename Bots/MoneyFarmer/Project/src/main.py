from wincaputil import *
from wizAPI import *
from moneyfarmer import MoneyFarmer

if(__name__ == '__main__'):
    try:
        windowInterface = wizAPI()
        windowInterface.register_window()

        bot = MoneyFarmer(windowInterface)
        bot.start()

    except WindowNotFoundException as e:
        print(e)