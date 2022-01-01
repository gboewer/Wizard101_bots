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

    def displayDetection(self):
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
            screenshot = self.renderedImageBorders(screenshot, 'Spells/Blizzard.png')
            screenshot = self.renderedImageBorders(screenshot, 'Spells/Blizzard_enchanted.png')
            screenshot = self.renderedImageBorders(screenshot, 'Spells/Epic.png')

        return screenshot
            
    def findImageCords(self, imagePath, threshold = 0.8, centered = True):
        screenshot = self.windowCapture.screenshot
        image = cv.imread(imagePath)

        imageBorders = self.findImageBorders(screenshot, image)
        if(not imageBorders is False):
            if(centered):
                cords = ((imageBorders[0] + imageBorders[2]) / 2, (imageBorders[1] + imageBorders[3]) / 2)
            else:
                cords = (imageBorders[0], imageBorders[1])
            return cords
        else: return False

    def findImageBorders(self, bigImage, smallImage, threshold = 0.8):
        result = cv.matchTemplate(bigImage, smallImage, cv.TM_CCOEFF_NORMED)
        minVal, maxVal, minCords, maxCords = cv.minMaxLoc(result)

        if(maxVal >= threshold):
            return (maxCords[0], maxCords[1], maxCords[0] + smallImage.shape[1], maxCords[1] + smallImage.shape[0])
        else: return False

    def renderedImageBorders(self, screenshot, imagePath):
        image = cv.imread(imagePath)

        imageBorders = self.findImageBorders(screenshot, image)
        if(imageBorders):
            topLeft = (imageBorders[0], imageBorders[1])
            topRight = (imageBorders[2], imageBorders[3])
            cv.rectangle(screenshot, topLeft, topRight, color = (0, 255, 0), thickness = 2, lineType = cv.LINE_4)

        return screenshot

    def checkPixel(self, x, y, controlPixelColorString):
        screenshot = self.windowCapture.screenshot
        pixelColor = screenshot[y][x]
        r, g, b = pixelColor
        pixelColorString = str(r) + ',' + str(g) + "," + str(b)
        return pixelColorString == controlPixelColorString