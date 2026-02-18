from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load model
with open("fake_review_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

print("Model loaded successfully")

@app.route("/")
def home():
    return "Fake Review Detection API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "reviewText" not in data:
        return jsonify({"error": "reviewText required"}), 400

    review = data["reviewText"]

    vec = vectorizer.transform([review])
    prediction = model.predict(vec)[0]
    confidence = model.predict_proba(vec)[0].max()

    return jsonify({
        "isFake": bool(prediction),
        "confidenceScore": round(confidence * 100, 2)
    })

if __name__ == "__main__":
    app.run(port=5001)
