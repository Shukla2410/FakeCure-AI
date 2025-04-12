import json
import os
import difflib

# Load trusted fake-real data once
def load_trusted_data():
    path = os.path.join(os.path.dirname(__file__), "..", "trusted_data.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

trusted_dataset = load_trusted_data()

# Check if input text matches any known fake claims
def check_fake_health_info(text):
    text_lower = text.lower()
    best_match = None
    best_score = 0.0

    for item in trusted_dataset:
        fake_lower = item["fake"].lower()
        score = difflib.SequenceMatcher(None, text_lower, fake_lower).ratio()
        if score > best_score:
            best_score = score
            best_match = item

    if best_score > 0.6:
        return {
            "status": "🚨 Potential Fake Health Claim Detected!",
            "suggestion": f'✅ Trusted Info: {best_match["real"]}'
        }
    else:
        return {
            "status": "✅ This doesn't match any known fake health claims.",
            "suggestion": "However, always verify health information with WHO or government health sites."
        }
