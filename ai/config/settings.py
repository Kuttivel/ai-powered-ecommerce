import os
from dotenv import load_dotenv

load_dotenv()

def load_settings():
    settings = {
        # Port for ai microservices written in '.env'
        "AI_PORT": int(os.getenv("AI_PORT", "5001")),
        
        # Mongo connection string
        "MONGO_URI": os.getenv("MONGO_URI"),
        
        # Mongo database
        "MONGO_DB": os.getenv("MONGO_DB", "lab_center"),
        
        # MongoDB 'product' collection 
        "MONGO_COLLECTION_PRODUCTS": os.getenv("MONGO_COLLECTION_PRODUCTS", "products"),
        
        # MongoDB 'chat_logs' collection
        "MONGO_COLLECTION_CHATLOGS": os.getenv("MONGO_COLLECTION_CHATLOGS", "chat_logs"),
        
        # MongoDB 'chat_sessions' collection
        "MONGO_COLLECTION_CHATSESSIONS": os.getenv("MONGO_COLLECTION_CHATSESSIONS", "chat_sessions"),
        
        # Path for Feature 1's 'fake_review_model.pkl' file
        "FEATURE_1_MODEL_PATH": os.getenv("FEATURE_1_MODEL_PATH", "models/feature_1/fake_review_model.pkl",), 
               
        # Path for Feature 1's 'fake_review_vectorizer.pkl' file
        "FEATURE_1_VECTORIZER_PATH": os.getenv("FEATURE_1_VECTORIZER_PATH", "models/feature_1/fake_review_vectorizer.pkl",),
        
        # Path for Feature 1's 'training_metrics.json' file
        "FEATURE_1_METRICS_PATH": os.getenv("FEATURE_1_METRICS_PATH", "models/feature_1/training_metrics.json",),
        
        # Path for Feature 1's dataset
        "FEATURE_1_DATASET_PATH": os.getenv("FEATURE_1_DATASET_PATH", "../datasets/fake reviews dataset.csv",),
        
        # Path for Feature 3's dataset
        "FEATURE_3_DATASET_PATH": os.getenv("FEATURE_3_DATASET_PATH", "../datasets/flipkart_com-ecommerce_sample.csv",),
        
        # Currency change from 'INR' to 'GBP' for simplicity
        "INR_TO_GBP_RATE": float(os.getenv("INR_TO_GBP_RATE", "0.0081")),
    }
    
    return settings