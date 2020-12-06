import cv2
from google.cloud import vision


class HandWritingRecognition:
    def __init__(self, nameImage, amountImage):
        self.nameImage = nameImage
        self.amountImage = amountImage
        self.client = vision.ImageAnnotatorClient()

    # Return ImageObject to be passed to visionApi
    def imageObjectCreation(self, ocrImage):
        imageString = cv2.imencode(".jpg", ocrImage)[1].tostring()
        imageObject = vision.Image(content=imageString)
        return imageObject

    # Return the text part of Response
    def printResponseText(self, response):
        docText = response.full_text_annotation.text
        return docText

    # Return Name from Image
    def nameOCR(self):
        nameObject = self.imageObjectCreation(self.nameImage)
        response = self.client.document_text_detection(image=nameObject)
        return self.printResponseText(response)

    # Return Amount from Image
    def amountOCR(self):
        amountObject = self.imageObjectCreation(self.amountImage)
        response = self.client.text_detection(image=amountObject)
        return self.printResponseText(response)
