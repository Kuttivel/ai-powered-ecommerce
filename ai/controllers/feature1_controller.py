from flask import request, jsonify, current_app
from services.feature1_service import predict_review

def feature1_health():
    return jsonify({
        "status": "ok",
        "feature": "feature_1_fake_review_detection",
    })

def predict_new_review():
    data = request.get_json()

    if not data:
        return jsonify({"Error: Input data missing"}), 400

    review_text = data.get("review_text")
    rating = data.get("rating")

    if review_text is None:
        return jsonify({"Error": "Field 'review_text' is required"}), 400

    if not isinstance(review_text, str):
        return jsonify({"Error": "Field 'review_text' must be a string"}), 400

    if review_text.strip() == "":
        return jsonify({"Error": "Field 'review_text' must not be empty"}), 400

    if rating is None:
        return jsonify({"message": "Field 'rating' is required"}), 400
    
    if not isinstance(rating, int):
        return jsonify({"message": "Field 'rating' must be an integer"}), 400
    
    if rating < 1 or rating > 5:
        return jsonify({"message": "Field 'rating' must be between 1 and 5"}), 400

    settings = current_app.settings

    try:
        result = predict_review(review_text, rating, settings)
        return jsonify(result), 200
    
    except FileNotFoundError as error:
        return jsonify({"message": str(error)}), 500
    
    except Exception as error:
        return jsonify({"message": f"Feature 1 prediction failed: {error}"}), 500