import win32gui
import cv2 as cv
from wizAPI import *
from moneyFarmer import *
from windowCapture import *
from detection import *

class WindowNotFoundException(Exception): pass

if(__name__ == '__main__'):
    try:
        DEBUG = True

        WINDOWNAME = 'Wizard101'
        windowHandle = win32gui.FindWindow(None, WINDOWNAME)
        if not windowHandle:
            raise WindowNotFoundException()

        if not windowHandle == win32gui.GetForegroundWindow():
            pyautogui.press('alt')
            win32gui.SetForegroundWindow(windowHandle)
            pyautogui.press('alt')

        windowCapture = WindowCapture(windowHandle)

        detection = Detection(windowCapture)

        bot = MoneyFarmer(windowCapture, detection)

        windowCapture.start()
        bot.start()

        def printInfo(event,x,y,flags,param):
                if event == cv.EVENT_LBUTTONDBLCLK:
                    if(not windowCapture.screenshot is None):
                        r, g, b = windowCapture.screenshot[y][x]
                        print(str(x) + ',' + str(y) + ': ' + str(r) + ',' + str(g) + ',' + str(b))

        DISPLAYWINDOWNAME = 'Window Feed'
        cv.namedWindow(DISPLAYWINDOWNAME)
        cv.setMouseCallback(DISPLAYWINDOWNAME, printInfo)

        while(True):
            debugScreenshot = detection.debugDetection()

            if(not debugScreenshot is False):
                cv.imshow(DISPLAYWINDOWNAME, debugScreenshot)

            if(cv.waitKey(1) == ord('q')):
                windowCapture.stop()
                bot.stop()
                cv.destroyAllWindows()
                break

    except WindowNotFoundException:
        print('Window not found')

    print('Bot terminated')
