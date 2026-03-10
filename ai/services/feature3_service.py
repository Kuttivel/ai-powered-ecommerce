import re
from bson import ObjectId
from datetime import datetime
from utils.nlp import (
    get_original_keywords,
    get_stemmed_keywords,
    remove_duplicate_words,
    get_price_limit,
    get_price_intent,
)


def create_session_if_needed(session_id, mongo):
    chat_sessions = mongo["chat_sessions"]

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
        }
    )

    return new_session_id


def save_chat_log(session_id, role, message, mongo):
    chat_logs = mongo["chat_logs"]

    chat_logs.insert_one(
        {
            "session_id": session_id,
            "role": role,
            "message": message,
            "created_at": datetime.utcnow(),
        }
    )

    mongo["chat_sessions"].update_one(
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


def apply_price_filter(products, price_limit, price_intent):
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


def search_products(original_keywords, mongo):
    products = mongo["products"]
    search_text = " ".join(original_keywords).strip()

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

    if search_text != "":
        text_results = list(
            products.find(
                {"$text": {"$search": search_text}},
                {**projection, "score": {"$meta": "textScore"}},
            )
            .sort([("score", {"$meta": "textScore"})])
            .limit(10)
        )

        if len(text_results) > 0:
            return text_results

    regex_conditions = build_regex_conditions(original_keywords)

    if len(regex_conditions) > 0:
        regex_results = list(
            products.find({"$or": regex_conditions}, projection).limit(10)
        )

        if len(regex_results) > 0:
            return regex_results

    return list(products.find({}, projection).limit(10))


def sort_products(products):
    return sorted(
        products,
        key=lambda product: (
            product.get("price") is None,
            product.get("price", 999999),
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
        return "I could not find matching products right now."

    keyword_text = ", ".join(keywords) if len(keywords) > 0 else "your request"

    if price_limit is not None:
        return f"I found {len(products)} products related to {keyword_text} under £{int(price_limit)}."

    if price_intent == "cheap":
        return f"I found {len(products)} budget-friendly products related to {keyword_text}."

    if price_intent == "expensive":
        return f"I found {len(products)} premium products related to {keyword_text}."

    if len(products) == 1:
        return f"I found 1 product related to {keyword_text}."

    return f"I found {len(products)} products related to {keyword_text}."


def process_chat_message(message, session_id, mongo):
    session_id = create_session_if_needed(session_id, mongo)
    save_chat_log(session_id, "user", message, mongo)

    original_keywords = remove_duplicate_words(get_original_keywords(message))
    stemmed_keywords = remove_duplicate_words(get_stemmed_keywords(message))
    price_limit = get_price_limit(message)
    price_intent = get_price_intent(message)

    products = search_products(original_keywords, mongo)
    products = apply_price_filter(products, price_limit, price_intent)
    products = sort_products(products)[:5]

    formatted_products = [format_product(product) for product in products]
    reply = build_reply(formatted_products, original_keywords, price_limit, price_intent)

    save_chat_log(session_id, "assistant", reply, mongo)

    return {
        "session_id": session_id,
        "message": message,
        "reply": reply,
        "keywords": original_keywords,
        "stemmed_keywords": stemmed_keywords,
        "price_limit": price_limit,
        "price_intent": price_intent,
        "total_products": len(formatted_products),
        "products": formatted_products,
    }