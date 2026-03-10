from flask import Blueprint
from controllers.feature3_controller import feature3_health, chat_with_assistant

feature3_bp = Blueprint("feature3", __name__)


@feature3_bp.route("/health", methods=["GET"])
def health():
    return feature3_health()


@feature3_bp.route("/chat", methods=["POST"])
def chat():
    return chat_with_assistant()