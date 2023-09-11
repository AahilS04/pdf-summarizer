import io
import os
from google.cloud import vision
from google.cloud import vision_v1
from importlib.resources import path
from pdf2image import convert_from_path

# import pandas as pd
# import gensim #the library for Topic modelling
# from gensim.utils import simple_preprocess
# from gensim.parsing.preprocessing import STOPWORDS
# from nltk.stem import WordNetLemmatizer, SnowballStemmer
# from nltk.stem.porter import *
# import numpy as np
# np.random.seed(400)
# import nltk
# nltk.download('wordnet')

# from sklearn.datasets import fetch_20newsgroups
# newsgroups_train = fetch_20newsgroups(subset='train', shuffle = True)
# newsgroups_test = fetch_20newsgroups(subset='test', shuffle = True)



from google.cloud.vision_v1 import types



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'src\serious-trainer-398717-bb803e2f7bed.json'

#r'pdf-summarizer\src\visionapitest-391318-5c97351e4624.json'

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
# pageList = []

# stemmer = SnowballStemmer("english")
# original_words = ['caresses', 'flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned', 
#            'humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational', 
#            'traditional', 'reference', 'colonizer','plotted']
# singles = [stemmer.stem(plural) for plural in original_words]

# pd.DataFrame(data={'original word':original_words, 'stemmed':singles })


# def lemmatize_stemming(text):
#     return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
# # Tokenize and lemmatize
# def preprocess(text):
#     result=[]
#     for token in gensim.utils.simple_preprocess(text) :
#         if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
#             result.append(lemmatize_stemming(token))
            
#     return(result)

#Reading PDF and scanning text.
pdf_path = r"pdf-summarizer/tests/AWS Cloud Practitioner.pdf"
pages = convert_from_path(pdf_path = pdf_path, poppler_path = poppler_path)
saving_folder = r"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output"
c = 1
processed_text = []
for page in pages: 
    img_name = f"img-{c}.jpeg"
    page.save(os.path.join(saving_folder,img_name),"JPEG")
    c+=1
    print(detect_document(rf"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output\{img_name}"))
    # # pageList.append(detect_document(rf"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output\{img_name}"))
    # text1 = lemmatize_stemming(detect_document(rf"C:\Users\aahil\OneDrive\Desktop\Projects\Noteshare\note_share-1\pdf-summarizer\output\{img_name}"))
    # processed_text.append(preprocess(text1))
    
# dictionary = gensim.corpora.Dictionary(processed_text)
# dictionary.filter_extremes(no_below=1, no_above=0.1, keep_n= 100000)
# bow_corpus = [dictionary.doc2bow(doc) for doc in processed_text]
# document_num = len(processed_text)
# bow_doc_x = bow_corpus[1]

# for i in range(len(bow_doc_x)):
#     print("Word {} (\"{}\") appears {} time.".format(bow_doc_x[i][0], dictionary[bow_doc_x[i][0]], bow_doc_x[i][1]))

#print(list(newsgroups_train.target_names))
