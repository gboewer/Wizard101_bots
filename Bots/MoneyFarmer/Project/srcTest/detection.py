import cv2 as cv
from threading import Thread
import moneyFarmer

class Detection:

    running = False
    botState = None
    windowCapture = None

    def __init__(self, windowCapture):
        self.windowCapture = windowCapture

    def start(self):
        self.running = True
        t = Thread(target=self.run)
        t.start()
        
    def run(self):
            while(self.running):
                pass
            
    def stop(self):
        self.running = False

    def setState(self, botState):
        self.botState = botState

    def debugDetection(self):
        screenshot = self.windowCapture.screenshot
        if(screenshot is None):
            return False

        if(type(self.botState) == moneyFarmer.Init):
            pass
        elif(type(self.botState) == moneyFarmer.WaitingScreen):
            pass
        elif(type(self.botState) == moneyFarmer.RunForward):
            pass
        elif(type(self.botState) == moneyFarmer.Fight):
            self.findImage('Spells/Blizzard.png', centered = False)
            self.findImage('Spells/Blizzard_enchanted.png', centered = False)
            self.findImage('Spells/Epic.png', centered = False)

        return screenshot
            
    def findImage(self, imagePath, threshold = 0.8, centered = True):
        screenshot = self.windowCapture.screenshot
        image = cv.imread(imagePath)

        result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)
        minVal, maxVal, minCords, maxCords = cv.minMaxLoc(result)

        if(maxVal >= threshold):
            if(centered == False):
                return maxCords
            else: return (maxCords[0] + image.shape[1] / 2, maxCords[1] + image.shape[0] / 2)
        else: return False

    def renderedImageBorder(self, imagePath):
        cords = self.findImage(imagePath, centered = False)
        if(cords):
            image = cv.imread(imagePath)

            imWidth = image.shape[1]
            imHeight = image.shape[0]
            
            topLeft = cords
            topRight = (cords[0] + imWidth, cords[1] + imHeight)

            cv.rectangle(screenshot, topLeft, topRight, color = (0, 255, 0), thickness = 2, lineType = cv.Line_4)

            return screenshot

    def checkPixel(self, x, y, controlPixelColorString):
        screenshot = self.windowCapture.screenshot
        pixelColor = screenshot[y][x]
        r, g, b = pixelColor
        pixelColorString = str(r) + ',' + str(g) + "," + str(b)
        return pixelColorString == controlPixelColorString