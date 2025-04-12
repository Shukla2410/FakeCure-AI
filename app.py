from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from utils.detector import check_fake_health_info
from flask_cors import CORS
import pytesseract
from PIL import Image
from io import BytesIO
import json
import difflib

app = Flask(__name__)
CORS(app)

# Load trusted data from a JSON file
with open("trusted_data.json", "r", encoding='utf-8') as f:
    trusted_statements = json.load(f)
    from transformers import pipeline
    classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")


# Extract only trusted 'real' info from JSON
trusted_data = [{"statement": entry['real'], "url": entry.get('source', '')} for entry in trusted_statements]

vectorizer = TfidfVectorizer().fit([entry['statement'] for entry in trusted_data])
trusted_vectors = vectorizer.transform([entry['statement'] for entry in trusted_data])


# Helper to find best match from trusted data
def find_best_match(user_text):
    texts = [entry['fake'] for entry in trusted_statements]
    best_match = difflib.get_close_matches(user_text, texts, n=1, cutoff=0.4)
    if best_match:
        for entry in trusted_statements:
            if entry['fake'] == best_match[0]:
                return entry['real']
    return "No trusted correction found."

def is_fake_news(text):
    result = classifier(text)
    label = result[0]['label']
    return label == 'FAKE'

def find_best_correction(text):
    user_vec = vectorizer.transform([text])
    similarities = cosine_similarity(user_vec, trusted_vectors)
    best_index = similarities.argmax()
    return trusted_data[best_index]

# Route to check text
@app.route("/text-check", methods=["POST"])
def text_check():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"status": "error", "suggestion": "No text provided."})

    if is_fake_news(text):
        correction = find_best_correction(text)
        return jsonify({
            "status": "❌ FAKE Information",
            "suggestion": correction['statement'],
            "source": correction['url']
        })
    else:
        return jsonify({
            "status": "✅ Seems Legit",
            "suggestion": "This looks like valid information from a trusted source."
        })

# Route to check image by OCR
@app.route("/image-check", methods=["POST"])
def image_check():
    if 'image' not in request.files:
        return jsonify({"result": "No image received."})

    image = Image.open(request.files['image'].stream)
    extracted_text = pytesseract.image_to_string(image)
    suggestion = find_best_match(extracted_text)
    status = "❌ FAKE Information" if suggestion != "No trusted correction found." else "✅ Seems Legit"

    return jsonify({"result": f"{status}\n\n{suggestion}"})

if __name__ == '__main__':
    app.run(debug=True)
