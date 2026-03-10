from flask import Flask, jsonify
from config.settings import load_settings
from config.database import get_mongo
from routes.feature1_route import feature1_bp
from routes.feature3_route import feature3_bp


def create_app():
    app = Flask(__name__)

    settings = load_settings()
    app.settings = settings 

    if settings["MONGO_URI"]:
        app.mongo = get_mongo(settings)  
    else:
        app.mongo = None  

    app.register_blueprint(feature1_bp, url_prefix="/api/feature-1")
    app.register_blueprint(feature3_bp, url_prefix="/api/feature-3")


    @app.route("/")
    def home():
        return jsonify({"message": "AI service is running", 
                        "features": ["Feature 1 - Fake Review Detection", 
                                     "Feature 3 - Conversational Product Search Assistant"]})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok",
                        "service": "ai"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=app.settings["AI_PORT"], debug=True)