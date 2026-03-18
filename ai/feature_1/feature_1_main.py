import pickle
import re
from scipy.sparse import csr_matrix, hstack
from nlp import clean_and_stem_text

model = None
vectorizer = None

SUSPICIOUS_PHRASES = {
    "highly recommend",
    "must buy",
    "best product",
    "best ever",
    "amazing product",
    "excellent product",
    "worth every penny",
    "value for money",
    "five stars",
    "100 percent",
    "totally satisfied",
    "superb product",
    "awesome product",
}

DETAIL_WORDS = {
    "delivery",
    "packaging",
    "quality",
    "material",
    "size",
    "fit",
    "colour",
    "color",
    "price",
    "comfortable",
    "battery",
    "screen",
    "sound",
    "design",
}



def load_feature_1_files(settings):
    global model, vectorizer

    if model is None:
        with open(settings["FEATURE_1_MODEL_PATH"], "rb") as model_file:
            model = pickle.load(model_file)

    if vectorizer is None:
        with open(settings["FEATURE_1_VECTORIZER_PATH"], "rb") as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)



def build_feature_1_input(review_text, rating):
    processed_text = clean_and_stem_text(review_text)

    x_text = vectorizer.transform([processed_text])
    x_rating = csr_matrix([[rating]])
    x_final = hstack([x_text, x_rating])

    return processed_text, x_final



def get_review_signals(review_text, rating):
    text = str(review_text).strip()
    lower_text = text.lower()
    words = re.findall(r"\b\w+\b", lower_text)

    exclamation_count = text.count("!")
    capital_word_count = len(re.findall(r"\b[A-Z]{3,}\b", text))
    repeated_characters = 1 if re.search(r"(.)\1\1", lower_text) else 0
    suspicious_phrase_count = sum(1 for phrase in SUSPICIOUS_PHRASES if phrase in lower_text)
    detail_word_count = sum(1 for word in DETAIL_WORDS if word in lower_text)

    word_count = len(words)
    unique_word_count = len(set(words))
    repeated_ratio = 0.0

    if word_count > 0:
        repeated_ratio = round(1 - (unique_word_count / word_count), 4)

    positive_word_hits = len(
        re.findall(r"\b(amazing|excellent|perfect|awesome|superb|best|fantastic|great)\b", lower_text)
    )
    negative_word_hits = len(
        re.findall(r"\b(but|however|issue|problem|slow|poor|bad|average)\b", lower_text)
    )

    return {
        "word_count": word_count,
        "exclamation_count": exclamation_count,
        "capital_word_count": capital_word_count,
        "repeated_characters": repeated_characters,
        "suspicious_phrase_count": suspicious_phrase_count,
        "detail_word_count": detail_word_count,
        "repeated_ratio": repeated_ratio,
        "positive_word_hits": positive_word_hits,
        "negative_word_hits": negative_word_hits,
        "rating": rating,
    }



def get_heuristic_adjustment(signals):
    adjustment = 0.0

    if signals["rating"] == 5 and signals["word_count"] <= 8:
        adjustment += 0.12

    if signals["word_count"] < 4:
        adjustment += 0.08

    if signals["exclamation_count"] >= 2:
        adjustment += 0.06

    if signals["capital_word_count"] >= 1:
        adjustment += 0.05

    if signals["repeated_characters"] == 1:
        adjustment += 0.05

    if signals["suspicious_phrase_count"] >= 1:
        adjustment += 0.18

    if signals["suspicious_phrase_count"] >= 2:
        adjustment += 0.08

    if signals["positive_word_hits"] >= 3:
        adjustment += 0.05

    if signals["repeated_ratio"] >= 0.35:
        adjustment += 0.04

    if signals["word_count"] >= 12:
        adjustment -= 0.05

    if signals["detail_word_count"] >= 2:
        adjustment -= 0.08

    if signals["negative_word_hits"] >= 1:
        adjustment -= 0.05

    return max(min(round(adjustment, 6), 0.4), -0.2)



def predict_review(review_text, rating, settings):
    load_feature_1_files(settings)

    processed_text, x_final = build_feature_1_input(review_text, rating)
    signals = get_review_signals(review_text, rating)

    model_prediction_code = int(model.predict(x_final)[0])
    probabilities = model.predict_proba(x_final)[0]

    model_prob_real = round(float(probabilities[0]), 6)
    model_prob_fake = round(float(probabilities[1]), 6)

    heuristic_adjustment = get_heuristic_adjustment(signals)

    final_prob_fake = model_prob_fake + heuristic_adjustment
    final_prob_fake = max(0.0, min(round(final_prob_fake, 6), 0.999999))
    final_prob_real = round(1 - final_prob_fake, 6)

    if 0.45 <= final_prob_fake <= 0.60:
        prediction_code = model_prediction_code
    else:
        prediction_code = 1 if final_prob_fake >= 0.60 else 0

    prediction_label = "Fake Review" if prediction_code == 1 else "Real Review"
    confidence_score = final_prob_fake if prediction_code == 1 else final_prob_real

    return {
        "prediction_code": prediction_code,
        "prediction_label": prediction_label,
        "prob_fake": final_prob_fake,
        "prob_real": final_prob_real,
        "confidence_score": confidence_score,
        "rating_used": rating,
        "processed_text": processed_text,
        "model_prob_fake": model_prob_fake,
        "model_prob_real": model_prob_real,
        "heuristic_adjustment": heuristic_adjustment,
        "review_signals": signals,
    }