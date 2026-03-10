import pickle
from scipy.sparse import csr_matrix, hstack
from utils.nlp import clean_and_stem_text

model = None
vectorizer = None


def load_feature1_files(settings):
    global model, vectorizer

    if model is None:
        with open(settings["FEATURE_1_MODEL_PATH"], "rb") as model_file:
            model = pickle.load(model_file)

    if vectorizer is None:
        with open(settings["FEATURE_1_VECTORIZER_PATH"], "rb") as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)

            
def build_feature_input(review_text, rating):
    processed_text = clean_and_stem_text(review_text)

    x_text = vectorizer.transform([processed_text])
    x_rating = csr_matrix([[rating]])

    x_final = hstack([x_text, x_rating])

    return processed_text, x_final


def predict_review(review_text, rating, settings):
    load_feature1_files(settings)

    processed_text, x_final = build_feature_input(review_text, rating)

    prediction_code = int(model.predict(x_final)[0])
    probabilities = model.predict_proba(x_final)[0]

    prob_real = round(float(probabilities[0]), 6)
    prob_fake = round(float(probabilities[1]), 6)

    prediction_label = "Fake Review" if prediction_code == 1 else "Real Review"
    confidence_score = prob_fake if prediction_code == 1 else prob_real

    return {
        "prediction_code": prediction_code,
        "prediction_label": prediction_label,
        "prob_fake": prob_fake,
        "prob_real": prob_real,
        "confidence_score": confidence_score,
        "rating_used": rating,
        "processed_text": processed_text
    }