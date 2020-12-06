# Cheque Verification

An attempt to completely automate cheque verification and money transfers in banks to reduce human labour.

Using computer vision, siamese networks and optical character recognition(OCR) to extract and process data from bank cheques, thereby automating the process of cheque verification in Banks.

## Tech Stack

- HTML
- CSS
- VANILLA JAVASCRIPT
- NODEJS
- EXPRESS
- PYTHON
- TENSORFLOW
- KERAS
- TESSERACT
- SQLITE
- VISION API

## Getting Started

Before we start the installation, first ensure that you have created a project on Google Cloud with **Vision API** enabled in it.
To do so follow this link [Quick Start Guide](https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-install-python).
Follow this guide till **Install the client library** section.

## Prerequisites

Ensure that your system have the following softwares
installed:

- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)
- [NodeJS](https://nodejs.org/en/download/)
- [Tesseract](https://tesseract-ocr.github.io/)

You can download them by clicking on the link.

## Installation

First download the Github Repository into your desired folder by using the following command.

> git clone https://github.com/Blastoise/Cheque-Verification.git

Now install all of the required Python libraries required to run the code using **_requirements.txt_** given in **_cheque-verification_** folder.

To do so, execute the following command:

> cd cheque-verification && pip3 install -r requirements.txt

Now we need to install all the required packages mentioned in **_package.json_** under **_cheque-verification-server_**.

Execute the following command and all the required packages will be installed and a **node_modules** folder would be created in **cheque-verification-server**.

> cd ../cheque-verification-server && npm install

You may need to give permission for running `npm install`.

Now copy the **mcr.trainedata** from **resources** folder into **tessdata** folder which would located inside the **Tesseract** folder where you have installed Tesseract.

In Windows, in general it is located at:

> **C:\Users\USER\AppData\Local\Tesseract-OCR\tessdata\mcr.traineddata**

In Linux and MacOs, in general it is located at:

> **/usr/share/tesseract-ocr/4.00/tessdata**

## Running the Application

To run the application, first go into **cheque-verification-server** folder and execute the **index.js** file using NodeJS.

To do so, execute the following (Assuming we are already in **cheque-verification-server** folder):

> node index.js

This will start the server at PORT _8000_.

Note: Keep all the cheques inside **_cheque_images_** under **_cheque-verification_** folder.

## Authors

- [Anil Muthigi](https://github.com/anilmuthigi)
- [Ashutosh Kumar](https://github.com/Blastoise)
- [Gaurav Bhagchandani](https://github.com/gauravbhag51)

## Important Links

- For downloading the Signature Data on which we trained, you can follow the link below:
  https://cedar.buffalo.edu/NIJ/data/signatures.rar

- Github Repo for mcr.tessdata: https://github.com/BigPino67/Tesseract-MICR-OCR
