import win32gui
import pyautogui
import time
import wincaputil
import windowcapture


class wizAPI:
    def __init__(self):
        self.windowHandle = None

    def register_window(self, name="Wizard101"):
        self.windowHandle = wincaputil.getWindowHandle(name)
        return

    def checkWindowFormat(self):
        wincaputil.checkWindowFormat(self.windowHandle)
        return self

    def screenshot(self):
        self.checkWindowFormat()
        windowCapture = windowcapture.WindowCapture(self.windowHandle)
        screenshot = windowCapture.get_screenshot()
        return screenshot

    def wait(self, s):
        """ Alias for time.sleep() that return self for function chaining """
        time.sleep(s)
        return self

    def is_active(self):
        """ Returns true if the window is focused """
        return self.windowHandle == win32gui.GetForegroundWindow()

    def set_active(self):
        """ Sets the window to active if it isn't already """
        if not self.is_active():
            """ Press alt before and after to prevent a nasty bug """
            pyautogui.press('alt')
            win32gui.SetForegroundWindow(self.windowHandle)
            pyautogui.press('alt')
        return self

    def get_window_rect(self):
        """Get the bounding rectangle of the window """
        rect = win32gui.GetWindowRect(self.windowHandle)
        return [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]

    def pixel_matches_color(self, coords, rgb, threshold=0):
        """ Matches the color of a pixel relative to the window's position """
        wx, wy = self.get_window_rect()[:2]
        x, y = coords
        # self.move_mouse(x, y)
        return pyautogui.pixelMatchesColor(x + wx, y + wy, rgb, tolerance=threshold)

    def move_mouse(self, x, y, speed=.5):
        """ Moves to mouse to the position (x, y) relative to the window's position """
        wx, wy = self.get_window_rect()[:2]
        pyautogui.moveTo(wx + x, wy + y, speed)
        return self

    def click(self, x, y, delay=.1, speed=.5, button='left'):
        """ Moves the mouse to (x, y) relative to the window and presses the mouse button """
        (self.set_active()
         .move_mouse(x, y, speed=speed)
         .wait(delay))

        pyautogui.click(button=button)
        return self

    def hold_key(self, key, holdtime):
        """ 
        Holds a key for a specific amount of time, usefull for moving with the W A S D keys 
        """
        self.set_active()
        pyautogui.keyDown(key)
        time.sleep(holdtime)
        pyautogui.keyUp(key)
        return self

    def press_key(self, key):
        """
        Presses a key, useful for pressing 'x' to enter a dungeon
        """
        self.set_active()
        pyautogui.press(key)
        return self