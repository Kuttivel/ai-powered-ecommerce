import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def prepare_nltk():
    try:
        stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")


prepare_nltk()

porter_stemmer = PorterStemmer()
english_stopwords = set(stopwords.words("english"))

extra_chat_stopwords = {
    "need",
    "want",
    "show",
    "find",
    "looking",
    "search",
    "please",
    "help",
    "give",
    "tell",
    "product",
    "products",
    "item",
    "items",
    "buy",
    "best",
    "good",
    "some",
    "me",
}


def clean_and_stem_text(text):
    text = re.sub("[^a-zA-Z]", " ", str(text))
    text = text.lower()
    words = text.split()

    words = [
        porter_stemmer.stem(word)
        for word in words
        if word not in english_stopwords
    ]

    return " ".join(words)


def get_original_keywords(text):
    text = re.sub("[^a-zA-Z0-9 £]", " ", str(text))
    text = text.lower()
    words = text.split()

    keywords = [
        word
        for word in words
        if word not in english_stopwords
        and word not in extra_chat_stopwords
        and len(word) > 1
    ]

    return keywords


def get_stemmed_keywords(text):
    original_keywords = get_original_keywords(text)

    stemmed_keywords = [
        porter_stemmer.stem(word)
        for word in original_keywords
    ]

    return stemmed_keywords


def remove_duplicate_words(words):
    seen = set()
    unique_words = []

    for word in words:
        if word not in seen:
            unique_words.append(word)
            seen.add(word)

    return unique_words


def get_price_limit(text):
    text = str(text).lower()

    match = re.search(r"(under|below|less than)\s*£?\s*(\d+)", text)
    if match:
        return float(match.group(2))

    match = re.search(r"£\s*(\d+)", text)
    if match and any(word in text for word in ["under", "below", "less than"]):
        return float(match.group(1))

    return None


def get_price_intent(text):
    text = str(text).lower()

    cheap_words = {"cheap", "budget", "low", "affordable"}
    expensive_words = {"premium", "expensive", "luxury", "costly"}

    if any(word in text.split() for word in cheap_words):
        return "cheap"

    if any(word in text.split() for word in expensive_words):
        return "expensive"

    return None