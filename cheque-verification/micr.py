import cv2
import pytesseract


class MICR:
    def __init__(self, imagePath):
        self.image = cv2.imread(imagePath)
        self.imageRGB = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    # Get index of the last digit from a String
    def getLastDigit(self, micrGroupArray):
        lastDigit = len(micrGroupArray) - 1
        while True:
            if micrGroupArray[lastDigit].isdigit() == True:
                break
            lastDigit -= 1
        return lastDigit

    # Return MICR code extracted from Cheque
    def extractMICR(self):
        micrImage = self.imageRGB[
            (-self.imageRGB.shape[0] // 7) :, 0 : self.imageRGB.shape[1]
        ]

        # Extracted Data from Tessaract
        micrGroupArray = pytesseract.image_to_string(micrImage, lang="mcr").split(" ")
        micrGroupArray = "".join(micrGroupArray)

        lastDigit = self.getLastDigit(micrGroupArray)

        firstPart = "c" + micrGroupArray[1:7] + "c"
        secondPart = micrGroupArray[8:17] + "a"
        thirdPart = micrGroupArray[lastDigit - 8 : lastDigit - 1]
        forthPart = micrGroupArray[lastDigit - 1 : lastDigit + 1]

        micrExtracted = firstPart + " " + secondPart + " " + thirdPart + " " + forthPart
        return micrExtracted
