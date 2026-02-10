import pandas as pd
from config.database import reviews_collection
from services.trainer import train_fake_review_model
from api.server import create_app

if __name__ == "__main__":

    reviews = list(reviews_collection.find(
        {"reviewText": {"$exists": True}, "rating": {"$ne": None}},
        {"_id": 0, "reviewText": 1, "rating": 1}
    ))

    df = pd.DataFrame(reviews)

    model, vectorizer = train_fake_review_model(df)

    app = create_app(model, vectorizer)

    print("AI Review Detection API running on http://localhost:5000")
    app.run(port=5000, debug=False)