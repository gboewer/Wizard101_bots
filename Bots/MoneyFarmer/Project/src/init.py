from botstatemachine import State
import cv2 as cv

class Init(State):
    def __init__(self, bot):
        super().__init__(bot)

    def enter(self): pass
    
    def run(self):
        cv.imshow('MoneyFarmer', self.bot.screenshot)

    def exit(self): pass