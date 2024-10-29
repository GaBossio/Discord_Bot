import os
import json
import random


class CustomContext:
    def __init__(self, interaction):
        self.author = interaction.user
        self.guild = interaction.guild
        self.channel = interaction.channel
        self.bot = interaction.client


def get_resource_path(file_name):
    # Get the absolute path of the base directory
    base_dir = os.path.abspath(os.getcwd())
    # Return the absolute path to the requested file
    return os.path.join(base_dir, "resources", "images" ,file_name)


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
