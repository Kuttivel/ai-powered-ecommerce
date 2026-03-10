from pymongo import MongoClient, TEXT

def get_mongo(settings):
    client = MongoClient(settings["MONGO_URI"])
    db = client[settings["MONGO_DB"]]
    products = db[settings["MONGO_COLLECTION_PRODUCTS"]]
    chat_logs = db[settings["MONGO_COLLECTION_CHATLOGS"]]
    chat_sessions = db[settings["MONGO_COLLECTION_CHATSESSIONS"]]
    
    # Text index for search
    try:
        products.create_index([("name", TEXT),
                               ("description", TEXT),
                               ("category", TEXT),
                               ("brand", TEXT),
                               ("tags", TEXT),], 
                               name="products_text_index")
    except Exception:
        pass
    
    return {
        "client": client,
        "db": db,
        "products": products,
        "chat_logs": chat_logs,
        "chat_sessions": chat_sessions,
    }