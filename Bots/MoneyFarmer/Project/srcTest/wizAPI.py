import win32gui
import pyautogui
import time
import cv2 as cv

class wizAPI:
    def __init__(self, windowHandle = None):
        self.windowHandle = windowHandle

    def displayScreenshot(self, windowName):
        if(self.screenshot.all != None):
            screenshotBGR = cv.cvtColor(self.screenshot, cv.COLOR_RGB2BGR)
            cv.imshow(windowName, screenshotBGR)

    def register_window(self, name="Wizard101"):
        self.windowHandle = wincaputil.getWindowHandle(name)
        return

    def checkWindowFormat(self):
        wincaputil.checkWindowFormat(self.windowHandle)
        return self

    def getScreenshot(self, update=True):
        self.checkWindowFormat()
        windowCapture = windowcapture.WindowCapture(self.windowHandle)
        screenshotBGR = windowCapture.get_screenshot()
        screenshotRGB = cv.cvtColor(screenshotBGR, cv.COLOR_BGR2RGB)
        if(update):
            self.screenshot = screenshotRGB
        return screenshotRGB

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
    
    def getPixelColorString(self, x, y):
        pixelColor = self.screenshot[y][x]
        r, g, b = pixelColor
        pixelColorString = str(r) + ',' + str(g) + "," + str(b)
        return pixelColorString

    def getPixelColorString(self, coords):
        x, y = coords
        pixelColor = self.screenshot[y][x]
        r, g, b = pixelColor
        pixelColorString = str(r) + ',' + str(g) + "," + str(b)
        return pixelColorString

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

    def hold_key_for_time(self, key, holdtime):
        """ 
        Holds a key for a specific amount of time, usefull for moving with the W A S D keys 
        """
        self.set_active()
        pyautogui.keyDown(key)
        time.sleep(holdtime)
        pyautogui.keyUp(key)
        return self

    def hold_key(self, key):
        self.set_active()
        pyautogui.keyDown(key)

    def unhold_key(self, key):
        self.set_active()
        pyautogui.keyUp(key)

    def press_key(self, key):
        """
        Presses a key, useful for pressing 'x' to enter a dungeon
        """
        self.set_active()
        pyautogui.press(key)
        return self

    def match_image(self, largeImg, smallImg, threshold=0.1, debug=False):
        """ Finds smallImg in largeImg using template matching """
        """ Adjust threshold for the precision of the match (between 0 and 1, the lowest being more precise """
        """ Returns false if no match was found with the given threshold """
        method = cv.TM_SQDIFF_NORMED

        # Read the images from the file
        small_image = cv.imread(smallImg)
        large_image = cv.imread(largeImg)
        w, h = small_image.shape[:-1]

        result = cv.matchTemplate(small_image, large_image, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv.minMaxLoc(result)

        if (mn >= threshold):
            return False

        # Extract the coordinates of our best match
        x, y = mnLoc

        if debug:
            # Draw the rectangle:
            # Get the size of the template. This is the same size as the match.
            trows, tcols = small_image.shape[:2]

            # Draw the rectangle on large_image
            cv.rectangle(large_image, (x, y),
                          (x+tcols, y+trows), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv.imshow('output', large_image)

            # The image is only displayed if we call this
            cv.waitKey(0)

        # Return coordinates to center of match
        return (x + (w * 0.5), y + (h * 0.5))

    def mouse_out_of_area(self, area):
        """ Move the mouse outside of an area, to make sure the mouse doesn't interfere with image matching """
        # Adjust the region so that it is relative to the window
        wx, wy = self.get_window_rect()[:2]
        region = list(area)
        region[0] += wx
        region[1] += wy

        def in_area(area):
            px, py = pyautogui.position()
            x, y, w, h = area
            return (px > x and px < (x + w) and py > y and py < (y + h))

        while in_area(region):
            pyautogui.moveRel(0, -100, duration=0.5)

        return self