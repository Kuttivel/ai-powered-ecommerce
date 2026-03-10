from flask import Blueprint
from controllers.feature1_controller import predict_new_review, feature1_health

feature1_bp = Blueprint("feature1", __name__)


@feature1_bp.route("/health", methods=["GET"])
def health():
    return feature1_health()


@feature1_bp.route("/predict", methods=["POST"])
def predict():
    return predict_new_review()