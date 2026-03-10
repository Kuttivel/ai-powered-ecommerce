import os
import sys
import pandas as pd
import re
from datetime import datetime, UTC

CURRENT_FILE_PATH = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CURRENT_FILE_PATH, "../..")))

from config.settings import load_settings
from config.database import get_mongo


settings = load_settings()
mongo = get_mongo(settings)
products_col = mongo["products"]
dataset_path = settings["FEATURE_3_DATASET_PATH"]
INR_TO_GBP_RATE = settings["INR_TO_GBP_RATE"]


def clean_price(value):
    if pd.isna(value):
        return None

    text = str(value).strip().replace("₹", "").replace(",", "")

    if text == "" or text.lower() in ["nan", "none", "null", "no price"]:
        return None

    try:
        return float(text)
    except Exception:
        return None


def convert_inr_to_gbp(price_inr):
    if price_inr is None:
        return None

    try:
        return round(float(price_inr) * INR_TO_GBP_RATE, 2)
    except Exception:
        return None


def format_gbp(price):
    if price is None:
        return None

    return f"£{price:.2f}"


def clean_description(desc):
    if pd.isna(desc):
        return ""

    text = str(desc)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_category_tree(cat_tree):
    if pd.isna(cat_tree):
        return "", ""

    text = str(cat_tree).strip()
    text = text.replace("[", "").replace("]", "").replace('"', "").replace("'", "")

    if "," in text:
        text = text.split(",")[0].strip()

    parts = [part.strip() for part in text.split(">>") if part.strip() != ""]

    if len(parts) == 0:
        return "", ""

    return parts[0], " > ".join(parts)


def clean_tags(specs):
    if pd.isna(specs):
        return []

    text = str(specs).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return [word for word in text.split(" ") if len(word) > 3][:15]


def clean_rating(value):
    if pd.isna(value):
        return None

    try:
        rating = float(value)
        if rating < 0 or rating > 5:
            return None
        return rating
    except Exception:
        return None


def main():
    df = pd.read_csv(dataset_path)

    total_rows = 0
    cleaned_rows = 0
    skipped_rows = 0
    product_docs = []

    print("Deleting old products from MongoDB...")
    delete_result = products_col.delete_many({})
    print("Old products deleted:", delete_result.deleted_count)

    for _, row in df.iterrows():
        total_rows += 1

        uniq_id = str(row.get("uniq_id", "")).strip()
        name = str(row.get("product_name", "")).strip()

        if name == "":
            skipped_rows += 1
            continue

        price_inr = clean_price(row.get("discounted_price"))
        if price_inr is None:
            price_inr = clean_price(row.get("retail_price"))

        if price_inr is None or price_inr <= 0:
            skipped_rows += 1
            continue

        price_gbp = convert_inr_to_gbp(price_inr)
        if price_gbp is None or price_gbp <= 0:
            skipped_rows += 1
            continue

        description = clean_description(row.get("description"))
        main_category, full_category_path = clean_category_tree(row.get("product_category_tree"))

        brand = str(row.get("brand", "")).strip()
        if brand.lower() in ["nan", "none", "null"]:
            brand = ""

        product_docs.append(
            {
                "uniq_id": uniq_id,
                "name": name,
                "price": price_gbp,
                "priceDisplay": format_gbp(price_gbp),
                "currency": "GBP",
                "originalPriceInr": price_inr,
                "description": description,
                "category": main_category,
                "categoryPath": full_category_path,
                "brand": brand,
                "imageUrl": str(row.get("image", "")).strip(),
                "rating": clean_rating(row.get("product_rating")),
                "overall_rating": clean_rating(row.get("overall_rating")),
                "tags": clean_tags(row.get("product_specifications")),
                "stock": 50,
                "createdAt": datetime.now(UTC),
                "updatedAt": datetime.now(UTC),
            }
        )
        cleaned_rows += 1

    if len(product_docs) > 0:
        products_col.insert_many(product_docs)

    print("Total rows in CSV:", total_rows)
    print("Products inserted:", cleaned_rows)
    print("Skipped rows:", skipped_rows)
    print("Collection:", settings["MONGO_COLLECTION_PRODUCTS"])


if __name__ == "__main__":
    main()