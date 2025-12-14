import os
import re
import json
from tkinter import messagebox
from Engine.Functions.TempSave import save_temp_locations

def get_locations(self):
    # Read location data from TextBasedAdventure.js (javascript file)
    # make sure to separate the location itself and its properties for editing


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
        locations = game_data.get("locations", {})
        return locations
    except Exception as e:
        messagebox.showerror("Error", f"Could not parse gameData: {e}")
        return None
        
def get_location_details(self, location_id):
    if hasattr(self, "locations_data") and self.locations_data and location_id in self.locations_data:
        return self.locations_data[location_id]
    else:
        messagebox.showerror("Error", f"Location '{location_id}' not found.")
        return None

def add_another_location(self, location_id, location_data):
    if not hasattr(self, "locations_data") or self.locations_data is None:
        self.locations_data = {}
    self.locations_data[location_id] = location_data
    self.mark_unsaved_changes()
    save_temp_locations(self.locations_data, self.temp_path)

def save_locations(self, locations):
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

    # Update locations
    game_data["locations"] = locations

    # Dump back to JS object string
    new_game_data_str = json.dumps(game_data, indent=4)

    # Rebuild the JS file
    new_js_content = js_content[:match.start(2)] + new_game_data_str + js_content[match.end(2):]

    with open(js_file_path, "w", encoding="utf-8") as js_file:
        js_file.write(new_js_content)