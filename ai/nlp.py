import re
from nltk.stem.porter import PorterStemmer

try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is",
        "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with", "this", "you",
        "your", "we", "they", "our", "or", "but", "if", "then", "there", "their", "them", "i", "me",
        "my", "mine", "so", "than", "too", "very", "can", "could", "would", "should", "do", "does",
        "did", "have", "had", "having", "been", "being", "not", "no", "yes", "about", "into", "up",
        "down", "over", "under", "again", "more", "most", "some", "such", "only", "own", "same",
    }

porter_stemmer = PorterStemmer()

greeting_words = {
    "hi", "hello", "hey", "hii", "helo", "good morning", "good evening", "good afternoon"
}

thanks_words = {
    "thanks", "thank you", "thankyou", "thx"
}

goodbye_words = {
    "bye", "goodbye", "see you", "see ya"
}

help_words = {
    "help", "what can you do", "how can you help", "what do you do"
}

follow_up_words = {
    "cheaper", "cheap", "budget", "affordable",
    "premium", "expensive", "luxury",
    "more", "another", "others", "similar"
}

extra_chat_stopwords = {
    "show", "find", "need", "want", "please", "product", "products", "item", "items"
}

cheap_words = {"cheap", "budget", "affordable", "low", "lower", "cheaper"}
expensive_words = {"premium", "expensive", "luxury", "high", "higher"}

price_filter_words = {
    "under", "below", "less", "than", "over", "above", "more"
}


def normalize_text(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9£\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_and_stem_text(content):
    text = re.sub("[^a-zA-Z]", " ", str(content))
    text = text.lower()
    words = text.split()

    words = [
        porter_stemmer.stem(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)


def get_original_keywords(text):
    text = normalize_text(text)
    words = text.split()
    keywords = []

    for word in words:
        if word in stop_words:
            continue

        if word in extra_chat_stopwords:
            continue

        if word in cheap_words or word in expensive_words:
            continue

        if word in price_filter_words:
            continue

        if word.isdigit():
            continue

        if len(word) <= 1:
            continue

        keywords.append(word)

    return keywords


def get_stemmed_keywords(text):
    original_keywords = get_original_keywords(text)
    return [porter_stemmer.stem(word) for word in original_keywords]


def remove_duplicate_words(words):
    unique_words = []
    seen = set()

    for word in words:
        if word not in seen:
            unique_words.append(word)
            seen.add(word)

    return unique_words


def get_price_limit(text):
    text = normalize_text(text)

    match = re.search(r"(under|below|less than)\s*£?\s*(\d+)", text)
    if match:
        return float(match.group(2))

    match = re.search(r"(over|above|more than)\s*£?\s*(\d+)", text)
    if match:
        return float(match.group(2))

    return None


def get_price_intent(text):
    text = normalize_text(text)
    words = set(text.split())

    if any(phrase in text for phrase in ["under", "below", "less than"]):
        return "under"

    if any(phrase in text for phrase in ["over", "above", "more than"]):
        return "above"

    if words.intersection(cheap_words):
        return "cheap"

    if words.intersection(expensive_words):
        return "expensive"

    return None


def is_follow_up_message(text):
    text = normalize_text(text)
    words = set(text.split())
    return len(words.intersection(follow_up_words)) > 0


def detect_small_talk(text):
    normalized_text = normalize_text(text)

    if normalized_text in greeting_words:
        return "greeting"

    if normalized_text in thanks_words:
        return "thanks"

    if normalized_text in goodbye_words:
        return "goodbye"

    if normalized_text in help_words:
        return "help"

    return None