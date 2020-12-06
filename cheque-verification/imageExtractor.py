import cv2


class ImageExtractor:
    def __init__(self, currentWorkingDir, imagePath):
        self.currentWorkingDir = currentWorkingDir
        self.image = cv2.imread(imagePath)
        self.imgResized = cv2.resize(self.image, (920, 400))

    # Return Name Image extracted from Cheque
    def nameImage(self):
        nameExtractedImage = self.imgResized[80:125, 85:802]
        return nameExtractedImage

    # Return Amount Image extracted from Cheque
    def amountImage(self):
        amountExtractedImage = self.imgResized[147:185, 685:863]
        return amountExtractedImage

    # Return Path of Signature Image extracted from Cheque
    def signatureImage(self):
        signExtractedImage = self.imgResized[207:275, 549:900]
        cv2.imwrite(self.currentWorkingDir + "/garbage.jpg", signExtractedImage)
        return self.currentWorkingDir + "/garbage.jpg"
