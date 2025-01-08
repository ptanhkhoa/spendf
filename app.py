from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")  # Load SpaCy model

@app.route('/parse', methods=['POST'])
def parse_text():
    data = request.json
    user_input = data.get('text', '')

    if not user_input:
        return jsonify({'error': 'No text provided'}), 400

    # Process text with SpaCy
    doc = nlp(user_input)
    response = {
        'entities': [{'text': ent.text, 'label': ent.label_} for ent in doc.ents],
        'tokens': [token.text for token in doc]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
