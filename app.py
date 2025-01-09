import re
from flask import Flask, request, jsonify
from textblob import TextBlob
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# List of popular Vietnamese banks (extendable)
popular_banks = [
    "vietcombank", "vcb", "techcombank", "tcb", "agribank", "vib", "mbbank", "acb", "bidv", "vpbank",
    "vietinbank", "scb", "shinhan", "sacombank", "eximbank", "abbank", "hdbank", "ocb", "vietbank"
]

# Flask app initialization
app = Flask(__name__)

# Function to handle general user mistakes using TextBlob (spell check)
def correct_mistakes(text):
    blob = TextBlob(text)
    return str(blob.correct())  # TextBlob corrects common spelling mistakes

# Function to classify entities (amount, bank, interest, term)
def classify_entities(text):
    text = correct_mistakes(text)  # First, correct any spelling mistakes

    entities = {"term": None, "interest": None, "amount": None, "bank": None}

    # Check for banks (using exact or partial match)
    for bank in popular_banks:
        if re.search(r'\b' + re.escape(bank) + r'\b', text, re.IGNORECASE):
            entities["bank"] = bank
            break  # stop after finding the first match

    # Detect term (e.g., "4 tháng", "4 months")
    term_match = re.search(r'(\d+)\s*(tháng|month|months)', text, re.IGNORECASE)
    if term_match:
        entities["term"] = term_match.group(1)  # Capture the number (term)

    # Detect interest (percentage)
    interest_match = re.search(r'(\d+)\s*(%|percent)', text, re.IGNORECASE)
    if interest_match:
        entities["interest"] = interest_match.group(0)  # Capture the interest rate

    # Detect amount (e.g., "3 triệu", "3 million", etc.)
    amount_match = re.search(r'(\d+)\s*(trieu|million|thousand|tram|k|usd|vnd)', text, re.IGNORECASE)
    if amount_match:
        entities["amount"] = amount_match.group(1)  # Capture the amount

    return entities

@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json()
    text = data.get("text", "")

    entities = classify_entities(text)
    
    # Check for missing entities
    missing_fields = [key for key, value in entities.items() if value is None]

    response = {
        "entities": entities,
        "missing_fields": missing_fields,
        "message": f"Missing information: {', '.join(missing_fields)}. Please provide the missing details." if missing_fields else "All information received.",
        "version": "1.1.1"
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
