import os
from sys import argv
import database
import utilities
import micr
import imageExtractor
import handWritingRecognition
import signatureVerification


# Current Working Directory
currentWorkingDir = os.path.dirname(os.getcwd())
currentWorkingDir = os.path.join(currentWorkingDir, "cheque-verification")


# Connecting to Database
db = database.Database(currentWorkingDir)

# Receiver Account Number
receiverAccountNumber = int(argv[2])


# Image Path
imageDir = currentWorkingDir + "/cheque_images"
imagePath = os.path.join(imageDir, argv[1])

# MICR Object
micrCode = micr.MICR(imagePath)

# Extracted Micr from Cheque
micrString = micrCode.extractMICR()

# Micr Id (middle part of Micr)
micrId = micrString.split(" ")
micrId = micrId[1] + micrId[2]


# Get Details of the Payer from Database
payerDetails = db.micrToAccountDetails(micrId)

# Get name of receiver from account number
receiverName = db.accNumberToName(receiverAccountNumber)[0]


# ImageExtractor Object
imageExtractor = imageExtractor.ImageExtractor(currentWorkingDir, imagePath)

# Get name, amount and signature extracted from cheque
nameImage = imageExtractor.nameImage()
amountImage = imageExtractor.amountImage()
signatureImage = imageExtractor.signatureImage()

# HandWritingRecognition Object
handWritingRecog = handWritingRecognition.HandWritingRecognition(nameImage, amountImage)

# Name of the receiver in Cheque
nameInCheque = handWritingRecog.nameOCR()

# If names don't match exit the code
if not utilities.nameCheck(nameInCheque, receiverName):
    exit(1)


# Path of signature database
chequeInDatabase = currentWorkingDir + "/database_images/" + payerDetails[2] + ".jpg"

# Signature Verification Object
signatureVerification = signatureVerification.SignatureVerification(
    currentWorkingDir, chequeInDatabase, signatureImage
)

# if signature is fake
if signatureVerification.verifySignature() == 1:
    os.remove(currentWorkingDir + "/garbage.jpg")
    exit(1)

# Removing the temporary file garbage.jpg
os.remove(currentWorkingDir + "/garbage.jpg")


# Amount written on cheque
amountInCheque = handWritingRecog.amountOCR()
amountInCheque = utilities.amountStandarize(amountInCheque)

# if Money not sufficient in account, exit the code
if payerDetails[1] < amountInCheque:
    exit(1)

# Update the balance in Payer's as well as Receiver's Account
db.updateAmount(payerDetails[3], receiverAccountNumber, amountInCheque)
exit(0)
