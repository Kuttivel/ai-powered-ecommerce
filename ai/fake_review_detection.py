import os
import re
import dotenv
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
from flask import Flask, request, jsonify

dotenv.load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
print("MONGODB connected successfully!")

db = client["lab_center"]
reviews_collection = db["reviews"]

reviews = reviews_collection.find({
                                    "reviewText": {"$exists": True}, 
                                    "isFake": {"$ne": None}
                                  },
                                  {
                                    "_id": 0, 
                                    "reviewText": 1, 
                                    "isFake": 1
                                  })
reviews_list = list(reviews)
print(f"Total reviews loaded: {len(reviews_list)}")

df = pd.DataFrame(reviews_list)
df.dropna(subset=["reviewText", "isFake"], inplace=True)



def clean_review(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # remove URLs
    text = re.sub(r"[^a-z\s]", "", text)         # remove punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip()     # remove extra spaces
    return text


df["cleanReviewText"] = df["reviewText"].apply(clean_review)
df["label"] = df["isFake"].astype(int)

X = df["cleanReviewText"]
Y = df["label"]

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, Y)

print("Model trained successfully!")

Y_pred = model.predict(X_vec)

accuracy = accuracy_score(Y, Y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:\n")
print(classification_report(Y, Y_pred))


def detect_review(review_text):
    cleaned = clean_review(review_text)
    vec = vectorizer.transform([cleaned])

    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec)[0].max()

    return {
        "prediction": "FAKE" if prediction == 1 else "GENUINE",
        "confidence": round(probability * 100, 2)
    }
    

app = Flask(__name__)

@app.route("/predict-review", methods=["POST"])
def predict_review():
    data = request.get_json()

    if not data or "reviewText" not in data:
        return jsonify({"error": "reviewText required"}), 400

    result = detect_review(data["reviewText"])

    reviews_collection.update_one({
                                    "reviewText": data["reviewText"]
                                  },
                                  {
                                    "$set": {
                                                "isFake": True if result["prediction"] == "FAKE" else False,
                                                "confidenceScore": result["confidence"],
                                                "aiModel": "LogisticRegression"
                                            }
                                  })

    return jsonify({"reviewText": data["reviewText"],
                    "prediction": result["prediction"],
                    "confidence": result["confidence"]})
    
if __name__ == "__main__":
    print("Review Detection API running on http://127.0.0.1:5000/predict-review")
    app.run(port=5000, debug=False)