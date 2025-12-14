import os
import re
import json
from tkinter import messagebox
from Engine.Functions.TempFileFunctions import save_temp_characters

def get_characters(self):
    js_file_path = os.path.join(self.current_game_path, "TextBasedAdventure.js")
    if not os.path.exists(js_file_path):
        messagebox.showerror("Error", "TextBasedAdventure.js file not found.")
        return None

    with open(js_file_path, "r", encoding="utf-8") as js_file:
        js_content = js_file.read()

    # Extract the gameData object using regex
    match = re.search(
        r'const gameData\s*=\s*(\{.*?\});',
        js_content, re.DOTALL
    )
    if not match:
        messagebox.showerror("Error", "No gameData object found in TextBasedAdventure.js.")
        return None

    game_data_str = match.group(1)

    # Remove trailing commas
    game_data_str = re.sub(r',(\s*[}\]])', r'\1', game_data_str)

    # Convert JS object to JSON
    try:
        game_data = json.loads(game_data_str)
        characters = game_data.get("characters", {})
        return characters
    except Exception as e:
        messagebox.showerror("Error", f"Could not parse gameData: {e}")
        return None
        
def get_character_details(self, character_id):
    if hasattr(self, "characters_data") and self.characters_data and character_id in self.characters_data:
        return self.characters_data[character_id]
    else:
        messagebox.showerror("Error", f"Character '{character_id}' not found.")
        return None

def add_another_character(self, character_id, character_data):
    if not hasattr(self, "characters_data") or self.characters_data is None:
        self.characters_data = {}
    self.characters_data[character_id] = character_data
    self.mark_unsaved_changes()
    save_temp_characters(self.characters_data, self.temp_path)

def save_characters(self, characters):
    js_file_path = os.path.join(self.current_game_path, "TextBasedAdventure.js")
    if not os.path.exists(js_file_path):
        messagebox.showerror("Error", "TextBasedAdventure.js file not found.")
        return

    with open(js_file_path, "r", encoding="utf-8") as js_file:
        js_content = js_file.read()

    # Extract the entire gameData object
    match = re.search(
        r'(const gameData\s*=\s*)(\{.*?\})(\s*;)', js_content, re.DOTALL
    )
    if not match:
        messagebox.showerror("Error", "No gameData object found in TextBasedAdventure.js.")
        return

    prefix, game_data_str, suffix = match.groups()

    # Remove trailing commas for JSON parsing
    game_data_str_clean = re.sub(r',(\s*[}\]])', r'\1', game_data_str)

    try:
        game_data = json.loads(game_data_str_clean)
    except Exception as e:
        messagebox.showerror("Error", f"Could not parse gameData: {e}")
        return

    # Update characters
    game_data["characters"] = characters

    # Dump back to JS object string
    new_game_data_str = json.dumps(game_data, indent=4)

    # Rebuild the JS file
    new_js_content = js_content[:match.start(2)] + new_game_data_str + js_content[match.end(2):]

    with open(js_file_path, "w", encoding="utf-8") as js_file:
        js_file.write(new_js_content)