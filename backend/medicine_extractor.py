import easyocr
import numpy as np
import json
import spacy

# Load the spaCy model for general NER
nlp = spacy.load("en_core_web_sm")

# Load drug dictionary
with open('drugs.json', 'r') as f:
    drugs_dict = json.load(f)

def text_from_image(img):
    # Read the image file and convert to a format EasyOCR can process
    img_data = np.array(img.read())  # Read image data as numpy array
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader
    result = reader.readtext(img_data)  # Perform OCR on the image

    # Extract text from the result
    all_text = []
    for (bbox, text, prob) in result:
        all_text.append(text)  # Collect recognized text

    return all_text

def drug_extraction(img):
    all_text_as_list = text_from_image(img)  # Get text from image
    all_text = " ".join(all_text_as_list)  # Combine text into a single string

    # Use spaCy's NLP model to process the text and extract entities
    doc = nlp(all_text)
    drug_entities = []
    
    # Loop through the detected entities
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":  # 'PRODUCT' often includes drugs in general NER
            if ent.text.lower() in drugs_dict["drugs"]:  # Match against the drugs dictionary
                drug_entities.append(ent.text)
    
    print("Extracted Drug Entities:", drug_entities)
    return drug_entities

if __name__ == "__main__":
    # Use an image containing text for drug extraction
    # Example: img = open('image.jpg', 'rb')
    img = open('path_to_your_image.jpg', 'rb')  # Update the path to your image
    drug_extraction(img)
