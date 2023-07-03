#!/usr/bin/env python3

"""pdfSummarizer.py: This script summarizes text provided in a PDF file."""

import os
from importlib.resources import path
import io
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import nltk
import pytesseract
import re
import slate3k as slate
import pdf2image
import PyPDF2
import cv2
import numpy as np
import fitz
#from pytesseract import output
from pdf2image import convert_from_path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from PIL import Image
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

nltk.download("stopwords")
nltk.download("punkt")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'sanguine-theory-390422-c6fa85864ebb.json'

client = vision.ImageAnnotatorClient()

poppler_path = r"C:\Users\aahil\Downloads\Release-23.05.0-0 (1)\poppler-23.05.0\Library\bin"


def print_text(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for annotation in response.text_annotations:
        vertices = [f"({v.x},{v.y})" for v in annotation.bounding_poly.vertices]
        print(
            f"{repr(annotation.description):42}",
            ",".join(vertices),
            sep=" | ",
        )












def extractText(file):
    reader = PdfReader(file)  
# getting a specific page from the pdf file
    text = ""
    for page in reader.pages:
        text += page.extract_text()
  
    return text


def extractOCR(file):
    pdf_path = file;
    text = ""
    pages = convert_from_path(pdf_path = pdf_path, poppler_path = poppler_path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    saving_folder = r"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output"
    c = 1
    for page in pages:
        img_name = f"img-{c}.jpeg"
        page.save(os.path.join(saving_folder,img_name),"JPEG")
        c+=1

        img = cv2.imread(rf"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output\{img_name}")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
 
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
 
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)
        
        im2 = img.copy()

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = im2[y:y + h, x:x + w]    
            text += pytesseract.image_to_string(cropped)

    return text




def summarize(text):
    # Process text by removing numbers and unrecognized punctuation
    processedText = re.sub("’", "'", text)
    processedText = re.sub("[^a-zA-Z' ]+", " ", processedText)
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(processedText)

    # Normalize words with Porter stemming and build word frequency table
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        elif stemmer.stem(word) in freqTable:
            freqTable[stemmer.stem(word)] += 1
        else:
            freqTable[stemmer.stem(word)] = 1

    # Normalize every sentence in the text
    sentences = sent_tokenize(text)
    stemmedSentences = []
    sentenceValue = dict()
    for sentence in sentences:
        stemmedSentence = []
        for word in sentence.lower().split():
            stemmedSentence.append(stemmer.stem(word))
        stemmedSentences.append(stemmedSentence)

    # Calculate value of every normalized sentence based on word frequency table
    # [:12] helps to save space
    for num in range(len(stemmedSentences)):
        for wordValue in freqTable:
            if wordValue in stemmedSentences[num]:
                if sentences[num][:12] in sentenceValue:
                    sentenceValue[sentences[num][:12]] += freqTable.get(wordValue)
                else:
                    sentenceValue[sentences[num][:12]] = freqTable.get(wordValue)

    # Determine average value of a sentence in the text
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue.get(sentence)

    average = int(sumValues / len(sentenceValue))

    # Create summary of text using sentences that exceed the average value by some factor
    # This factor can be adjusted to reduce/expand the length of the summary
    summary = ""
    for sentence in sentences:
            if sentence[:12] in sentenceValue and sentenceValue[sentence[:12]] > (3.0 * average):
                summary += " " + " ".join(sentence.split())

    # Process the text in summary and write it to a new file
    summary = re.sub("’", "'", summary)
    summary = re.sub("[^a-zA-Z0-9'\"():;,.!?— ]+", " ", summary)
    # summaryText = open(fileName + "summary.txt", "w")
    # summaryText.write(summary)
    # summaryText.close()
    print(summary)


# Scan user input for PDF file name
print("What is the name of the PDF?")
fileName = input("(Without .pdf file extension)\n")
pdfFileName = fileName + ".pdf"
option = input("Direct text extraction or OCR extraction? (text / OCR)\n")

if option == "text":
    #text = extractText(pdfFileName)
    #summarize(text)
    image_uri = f'{pdfFileName}'
    features = [vision.Feature.Type.TEXT_DETECTION]

    response = analyze_image_from_uri(image_uri, features)
    print_text(response)
    #print(text)
elif option == "OCR":
    text = extractOCR(pdfFileName)
    print(text)
else:
    print("Not a valid option!")
