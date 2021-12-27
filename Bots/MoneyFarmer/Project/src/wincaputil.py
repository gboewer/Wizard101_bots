import win32gui, win32con

class WindowNotFoundException(Exception):
    def __init__(self, message): super().__init__(message)

class IncorrectWindowFormatException(Exception):
    def __init__(self, message): super().__init__(message)

class WindowClosedException(Exception):
    def __init__(self, message): super().__init__(message)

def getWindowHandle(windowName):
    windowHandle = win32gui.FindWindow(None, windowName)
    if not windowHandle:
        raise WindowNotFoundException('Error: Window not found')

    return windowHandle

def checkWindowFormat(windowHandle):
    tup = win32gui.GetWindowPlacement(windowHandle)
    if(not tup[1] == win32con.SW_SHOWNORMAL):
        raise IncorrectWindowFormatException('Error: Window is either minimized or maximized')