import os
import spacy
from flask import Flask, request, jsonify
import logging

# Initialize Flask app
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Try loading SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logging.info("SpaCy model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load SpaCy model: {e}")
    raise e

# Define the parsing route
@app.route("/parse", methods=["POST"])
def parse_text():
    try:
        # Get input text from the request
        data = request.json
        user_input = data.get("text", "")

        if not user_input:
            return jsonify({"error": "No text provided"}), 400

        # Process text with SpaCy
        doc = nlp(user_input)

        # Prepare the response
        response = {
            "entities": [{"text": ent.text, "label": ent.label_} for ent in doc.ents],
            "tokens": [token.text for token in doc]
        }
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in processing text: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

# Home route to verify app is running
@app.route("/")
def index():
    return "Flask app is running and ready to parse!"

# Run the app
if __name__ == "__main__":
    # Use the dynamic port provided by Render or default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
