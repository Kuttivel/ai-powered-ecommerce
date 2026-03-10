from flask import current_app, jsonify, request
from services.feature3_service import process_chat_message


def feature3_health():
    return jsonify({
        "status": "ok",
        "feature": "feature_3_conversational_assistant"
    })


def chat_with_assistant():
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

    mongo = current_app.mongo

    if mongo is None:
        return jsonify({"message": "MongoDB is not connected"}), 500

    result = process_chat_message(message, session_id, mongo)

    return jsonify(result), 200