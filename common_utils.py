import os
import json
import random


def get_random_response(category, subcategory):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "Discord_Bot", "resources", "responses.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return random.choice(data[category][subcategory])
    except (FileNotFoundError, KeyError) as e:
        return f"Error: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"
