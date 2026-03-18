from flask import Flask, jsonify, request
from config.settings import load_settings
from config.database import get_mongo
from feature_1.feature_1_main import predict_review
from feature_3.feature_3_main import process_chat_message


def create_app():
    app = Flask(__name__)

    settings = load_settings()
    app.settings = settings

    if settings["MONGO_URI"]:
        app.mongo = get_mongo(settings)
    else:
        app.mongo = None

    @app.route("/")
    def home():
        return jsonify({
            "message": "AI service is running",
            "features": [
                "Feature 1 - Fake Review Detection",
                "Feature 3 - Conversational Product Search Assistant",
            ],
        })

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "ai"})

    @app.route("/api/feature-1/health", methods=["GET"])
    def feature_1_health():
        return jsonify({"status": "ok", "feature": "feature_1_fake_review_detection"})

    @app.route("/api/feature-1/predict", methods=["POST"])
    def feature_1_predict():
        data = request.get_json()

        if not data:
            return jsonify({"message": "Input data is missing"}), 400

        review_text = data.get("review_text")
        rating = data.get("rating")

        if review_text is None:
            return jsonify({"message": "Field 'review_text' is required"}), 400

        if not isinstance(review_text, str):
            return jsonify({"message": "Field 'review_text' must be a string"}), 400

        if review_text.strip() == "":
            return jsonify({"message": "Field 'review_text' must not be empty"}), 400

        if rating is None:
            return jsonify({"message": "Field 'rating' is required"}), 400

        if not isinstance(rating, int):
            return jsonify({"message": "Field 'rating' must be an integer"}), 400

        if rating < 1 or rating > 5:
            return jsonify({"message": "Field 'rating' must be between 1 and 5"}), 400

        try:
            result = predict_review(review_text, rating, settings)
            return jsonify(result), 200
        except Exception as error:
            return jsonify({"message": f"Feature 1 prediction failed: {error}"}), 500

    @app.route("/api/feature-3/health", methods=["GET"])
    def feature_3_health():
        return jsonify({"status": "ok", "feature": "feature_3_conversational_product_search"})

    @app.route("/api/feature-3/chat", methods=["POST"])
    def feature_3_chat():
        data = request.get_json()

        if not data:
            return jsonify({"message": "Input data is missing"}), 400

        message = data.get("message")
        session_id = data.get("session_id")

        if message is None:
            return jsonify({"message": "Field 'message' is required"}), 400

        if not isinstance(message, str):
            return jsonify({"message": "Field 'message' must be a string"}), 400

        if message.strip() == "":
            return jsonify({"message": "Field 'message' must not be empty"}), 400

        if app.mongo is None:
            return jsonify({"message": "MongoDB is not connected"}), 500

        try:
            result = process_chat_message(message, session_id, app.mongo, settings)
            return jsonify(result), 200
        except Exception as error:
            return jsonify({"message": f"Feature 3 chat failed: {error}"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.settings["AI_PORT"],
        debug=app.settings["AI_DEBUG"],
    )