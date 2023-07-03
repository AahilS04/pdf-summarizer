import io
import os
from google.cloud import vision
from google.cloud import vision_v1
from importlib.resources import path
from pdf2image import convert_from_path


from google.cloud.vision_v1 import types



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'pdf-summarizer\src\visionapitest-391318-5c97351e4624.json'

client = vision.ImageAnnotatorClient()
poppler_path = r"C:\Users\aahil\Downloads\Release-23.05.0-0 (1)\poppler-23.05.0\Library\bin"


def detect_document(path):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient()
    text = ""

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                #print("Paragraph confidence: {}".format(paragraph.confidence))

                for word in paragraph.words:
                    text+= "".join([symbol.text for symbol in word.symbols])
                    text += " "
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return text

pdf_path = r"pdf-summarizer/tests/AWS Cloud Practitioner.pdf"
pages = convert_from_path(pdf_path = pdf_path, poppler_path = poppler_path)
saving_folder = r"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output"
c = 1
for page in pages: 
    img_name = f"img-{c}.jpeg"
    page.save(os.path.join(saving_folder,img_name),"JPEG")
    c+=1
    print(detect_document(rf"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output\{img_name}"))
    print("\n")
    
