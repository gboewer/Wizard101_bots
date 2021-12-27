from botstatemachine import State
import cv2 as cv

class Init(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): self.bot.windowInterface.press_key('x')
    
    def run(self):
        screenshot = self.bot.windowInterface.screenshot()
        cv.imshow('MoneyFarmer', screenshot)

    def exit(self): pass