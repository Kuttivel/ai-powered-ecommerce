import os
import re
from bson import ObjectId
from datetime import datetime
from nlp import (
    get_original_keywords,
    get_price_limit,
    get_price_intent,
    is_follow_up_message,
    remove_duplicate_words,
)
from feature_3.intent_helper import get_intent_reply



def create_session_if_needed(session_id, mongo, settings):
    chat_sessions = mongo[settings["MONGO_COLLECTION_CHATSESSIONS"]]

    if session_id:
        existing_session = chat_sessions.find_one({"session_id": session_id})
        if existing_session:
            return session_id

    new_session_id = str(ObjectId())

    chat_sessions.insert_one(
        {
            "session_id": new_session_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_keywords": [],
            "last_price_limit": None,
            "last_price_intent": None,
        }
    )

    return new_session_id



def get_session_context(session_id, mongo, settings):
    session = mongo[settings["MONGO_COLLECTION_CHATSESSIONS"]].find_one({"session_id": session_id})

    if not session:
        return {
            "last_keywords": [],
            "last_price_limit": None,
            "last_price_intent": None,
        }

    return {
        "last_keywords": session.get("last_keywords", []),
        "last_price_limit": session.get("last_price_limit"),
        "last_price_intent": session.get("last_price_intent"),
    }



def update_session_context(session_id, keywords, price_limit, price_intent, mongo, settings):
    mongo[settings["MONGO_COLLECTION_CHATSESSIONS"]].update_one(
        {"session_id": session_id},
        {
            "$set": {
                "updated_at": datetime.utcnow(),
                "last_keywords": keywords,
                "last_price_limit": price_limit,
                "last_price_intent": price_intent,
            }
        },
    )



def save_chat_log(session_id, role, message, mongo, settings):
    mongo[settings["MONGO_COLLECTION_CHATLOGS"]].insert_one(
        {
            "session_id": session_id,
            "role": role,
            "message": message,
            "created_at": datetime.utcnow(),
        }
    )

    mongo[settings["MONGO_COLLECTION_CHATSESSIONS"]].update_one(
        {"session_id": session_id},
        {"$set": {"updated_at": datetime.utcnow()}},
    )



def build_regex_conditions(keywords):
    conditions = []

    for keyword in keywords:
        safe_keyword = re.escape(keyword)
        conditions.append({"name": {"$regex": safe_keyword, "$options": "i"}})
        conditions.append({"description": {"$regex": safe_keyword, "$options": "i"}})
        conditions.append({"category": {"$regex": safe_keyword, "$options": "i"}})
        conditions.append({"brand": {"$regex": safe_keyword, "$options": "i"}})
        conditions.append({"tags": {"$regex": safe_keyword, "$options": "i"}})

    return conditions



def merge_with_session_context(message, session_context, keywords, price_limit, price_intent):
    follow_up = is_follow_up_message(message)

    if (len(keywords) == 0 or follow_up) and len(session_context["last_keywords"]) > 0:
        keywords = session_context["last_keywords"]

    if follow_up and price_limit is None and session_context["last_price_limit"] is not None:
        price_limit = session_context["last_price_limit"]

    if follow_up and price_intent is None and session_context["last_price_intent"] is not None:
        price_intent = session_context["last_price_intent"]

    text = str(message).lower()

    if any(word in text for word in ["cheaper", "cheap", "budget", "affordable"]):
        price_intent = "cheap"

    if any(word in text for word in ["premium", "expensive", "luxury"]):
        price_intent = "expensive"

    return keywords, price_limit, price_intent



def search_products(original_keywords, mongo, settings):
    products = mongo[settings["MONGO_COLLECTION_PRODUCTS"]]
    projection = {
        "name": 1,
        "description": 1,
        "category": 1,
        "brand": 1,
        "price": 1,
        "priceDisplay": 1,
        "currency": 1,
        "tags": 1,
        "imageUrl": 1,
        "rating": 1,
        "stock": 1,
    }

    search_text = " ".join(original_keywords).strip()

    if search_text:
        try:
            text_results = list(
                products.find(
                    {"$text": {"$search": search_text}},
                    {**projection, "score": {"$meta": "textScore"}},
                )
                .sort([("score", {"$meta": "textScore"})])
                .limit(20)
            )

            if text_results:
                return text_results
        except Exception:
            pass

    regex_conditions = build_regex_conditions(original_keywords)

    if regex_conditions:
        regex_results = list(products.find({"$or": regex_conditions}, projection).limit(20))
        if regex_results:
            return regex_results

    return list(products.find({}, projection).sort({"price": 1}).limit(10))



def apply_price_filter(products, price_limit, price_intent):
    if price_limit is not None and price_intent == "above":
        return [
            product
            for product in products
            if product.get("price") is not None and product.get("price") >= price_limit
        ]

    if price_limit is not None:
        return [
            product
            for product in products
            if product.get("price") is not None and product.get("price") <= price_limit
        ]

    if price_intent == "cheap":
        return [
            product
            for product in products
            if product.get("price") is not None and product.get("price") <= 50
        ]

    if price_intent == "expensive":
        return [
            product
            for product in products
            if product.get("price") is not None and product.get("price") >= 100
        ]

    return products



def score_product(product, keywords):
    score = 0

    name = str(product.get("name", "")).lower()
    description = str(product.get("description", "")).lower()
    category = str(product.get("category", "")).lower()
    brand = str(product.get("brand", "")).lower()
    tags = " ".join(product.get("tags", [])).lower()

    for keyword in keywords:
        if keyword in name:
            score += 5
        if keyword in category:
            score += 4
        if keyword in brand:
            score += 3
        if keyword in tags:
            score += 2
        if keyword in description:
            score += 1

    return score



def sort_products(products, keywords, price_intent):
    return sorted(
        products,
        key=lambda product: (
            -score_product(product, keywords),
            product.get("price") is None,
            product.get("price", 999999) if price_intent != "expensive" else -product.get("price", 0),
        ),
    )



def format_product(product):
    return {
        "id": str(product.get("_id")),
        "name": product.get("name"),
        "description": product.get("description"),
        "category": product.get("category"),
        "brand": product.get("brand"),
        "price": product.get("price"),
        "priceDisplay": product.get("priceDisplay"),
        "currency": product.get("currency"),
        "tags": product.get("tags", []),
        "imageUrl": product.get("imageUrl"),
        "rating": product.get("rating"),
        "stock": product.get("stock"),
    }



def build_reply(products, keywords, price_limit, price_intent):
    if len(products) == 0:
        return "I could not find matching products. Try a product name, brand, or a price range."

    top_products = products[:2]
    top_text = ", ".join(
        [f"{product.get('name')} ({product.get('priceDisplay')})" for product in top_products]
    )

    if price_limit is not None and price_intent == "above":
        return f"I found {len(products)} products above your price range. Top options are {top_text}."

    if price_limit is not None:
        return f"I found {len(products)} products within your price range. Top options are {top_text}."

    if price_intent == "cheap":
        return f"I found {len(products)} budget-friendly products. Top options are {top_text}."

    if price_intent == "expensive":
        return f"I found {len(products)} premium products. Top options are {top_text}."

    if keywords:
        return f"I found {len(products)} products related to {' '.join(keywords)}. Top options are {top_text}."

    return f"I found {len(products)} products. Top options are {top_text}."



def get_intent_json_path(settings):
    ai_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(ai_path, settings["INTENT_JSON_PATH"])



def process_chat_message(message, session_id, mongo, settings):
    session_id = create_session_if_needed(session_id, mongo, settings)
    save_chat_log(session_id, "user", message, mongo, settings)

    intent_result = get_intent_reply(message, get_intent_json_path(settings))

    if intent_result is not None:
        reply = intent_result["reply"]
        save_chat_log(session_id, "assistant", reply, mongo, settings)

        return {
            "session_id": session_id,
            "reply": reply,
            "products": [],
        }

    session_context = get_session_context(session_id, mongo, settings)

    original_keywords = remove_duplicate_words(get_original_keywords(message))
    price_limit = get_price_limit(message)
    price_intent = get_price_intent(message)

    original_keywords, price_limit, price_intent = merge_with_session_context(
        message,
        session_context,
        original_keywords,
        price_limit,
        price_intent,
    )

    if len(original_keywords) == 0 and price_limit is None and price_intent is None:
        reply = "Please tell me a product name, brand, or a price range such as under £20."
        save_chat_log(session_id, "assistant", reply, mongo, settings)
        return {
            "session_id": session_id,
            "reply": reply,
            "products": [],
        }

    matched_products = search_products(original_keywords, mongo, settings)
    matched_products = apply_price_filter(matched_products, price_limit, price_intent)
    matched_products = sort_products(matched_products, original_keywords, price_intent)

    final_products = matched_products[:5]
    reply = build_reply(final_products, original_keywords, price_limit, price_intent)

    update_session_context(session_id, original_keywords, price_limit, price_intent, mongo, settings)
    save_chat_log(session_id, "assistant", reply, mongo, settings)

    return {
        "session_id": session_id,
        "reply": reply,
        "products": [format_product(product) for product in final_products],
    }