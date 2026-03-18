import json
import os
import random

from config.settings import load_settings

settings = load_settings()


def load_intents(intent_json_path=None):
    if intent_json_path is None:
        ai_path = os.path.dirname(os.path.dirname(__file__))
        intent_json_path = os.path.join(ai_path, settings["INTENT_JSON_PATH"])

    with open(intent_json_path, "r", encoding="utf-8") as intent_file:
        return json.load(intent_file)



def get_intent_reply(message_text, intent_json_path=None):
    message_text = str(message_text).strip().lower()
    intents = load_intents(intent_json_path)

    for intent_name, intent_data in intents.items():
        patterns = intent_data.get("patterns", [])
        responses = intent_data.get("responses", [])

        for pattern in patterns:
            if message_text == pattern.strip().lower():
                if responses:
                    return {
                        "intent": intent_name,
                        "reply": random.choice(responses),
                    }

    return Non