import spacy
from flask import Flask, request, jsonify
import re

# Load SpaCy model (ensure it's installed in the environment)
nlp = spacy.load("en_core_web_sm")  # You can adjust the language model if needed

# Predefined list of popular Vietnamese banks
popular_banks = [
    "vietcombank", "vcb", "techcombank", "tcb", "agribank", "vib", "mbbank", "acb", "vib", "bidv",
    "vpbank", "vietinbank", "scb", "shinhan", "sacombank", "eximbank", "abbank", "hdbank", "ocb", "vietbank", "mbbank"
]

# Flask app initialization
app = Flask(__name__)

# Track version
version = "1.1.0"  # You can update this whenever you make changes to the app

def classify_entities(text):
    doc = nlp(text)
    
    entities = {"term": None, "interest": None, "amount": None, "bank": None}
    
    # Simple rules to classify entities based on the text
    for ent in doc.ents:
        if ent.label_ == "CARDINAL":
            # If the word "tháng" is in the sentence, classify as term
            if "tháng" in text or "month" in text:  # term context
                entities["term"] = ent.text
            # If the word "trieu", "million", "tram", "thousand" is in the sentence, classify as amount
            elif "trieu" in text or "million" in text or "tram" in text or "thousand" in text:  # amount context
                entities["amount"] = ent.text
        elif ent.label_ == "PERCENT":
            # Recognize interest
            entities["interest"] = ent.text
        elif ent.text.lower() in popular_banks:
            # Recognize bank names
            entities["bank"] = ent.text.lower()
    
    return entities

@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json()
    text = data.get("text", "")
    
    entities = classify_entities(text)
    
    # Check for missing entities and return appropriate response
    missing_fields = [key for key, value in entities.items() if value is None]
    
    response = {
        "entities": entities,
        "missing_fields": missing_fields,
        "version": version  # Return the version of the app
    }

    # Check if the bank is not recognized
    if entities["bank"] is None:
        response["message"] = "Bank not recognized. Would you like to add a new bank?"

    # If any fields are missing, ask the user to fill in the missing data
    if missing_fields:
        response["message"] = f"Missing information: {', '.join(missing_fields)}. Please provide the missing details."
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
