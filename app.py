from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import underthesea

app = Flask(__name__)

# Load PhoBERT model and tokenizer
MODEL_NAME = "vinai/phobert-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

# Define processing pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Popular Vietnamese banks and aliases
BANKS = {
    "vietcombank": ["vcb", "ngoai thuong", "vietcombank"],
    "techcombank": ["tcb", "ky thuong", "techcombank"],
    "agribank": ["nong nghiep", "agribank"],
    "vib": ["quoc te", "vib"],
    # Add more banks here...
}

def normalize_number(text):
    """Convert Vietnamese text numbers to integers (e.g., 'ba triệu' → 3000000)."""
    return underthesea.text_to_number(text)

def detect_missing_fields(entities):
    """Detect missing fields from extracted entities."""
    required_fields = {"amount", "term", "interest", "bank"}
    missing = required_fields - set(entities.keys())
    return list(missing)

@app.route("/process", methods=["POST"])
def process_text():
    data = request.json
    text = data.get("input", "")
    if not text:
        return jsonify({"error": "Input text is required"}), 400

    # Extract entities using PhoBERT
    ner_results = ner_pipeline(text)
    entities = {"amount": None, "term": None, "interest": None, "bank": None}

    # Process recognized entities
    for entity in ner_results:
        label = entity["entity_group"].lower()
        value = entity["word"].strip()
        if label == "amount":
            entities["amount"] = normalize_number(value)
        elif label == "term":
            entities["term"] = normalize_number(value)
        elif label == "interest":
            entities["interest"] = value
        elif label == "bank":
            for bank, aliases in BANKS.items():
                if any(alias in value.lower() for alias in aliases):
                    entities["bank"] = bank
                    break

    # Detect missing fields
    missing_fields = detect_missing_fields(entities)

    return jsonify({
        "entities": entities,
        "message": f"Missing information: {', '.join(missing_fields)}. Please provide the missing details."
        if missing_fields else "All required fields are provided.",
        "missing_fields": missing_fields,
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
