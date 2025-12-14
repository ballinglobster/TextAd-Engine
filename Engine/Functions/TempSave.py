import os
import json

# TEMPORARY SAVING FUNCTIONS    
def save_temp_locations(locations_data, temp_path):
    temp_file = os.path.join(temp_path, "temp_locations.json")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(locations_data, f, indent=4)

def save_temp_items(items_data, temp_path):
    temp_file = os.path.join(temp_path, "temp_items.json")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(items_data, f, indent=4)

def save_temp_characters(characters_data, temp_path):
    temp_file = os.path.join(temp_path, "temp_characters.json")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(characters_data, f, indent=4)

# CLEAR TEMP FILES  
def clear_temp_files(temp_path):
    temp_locations_file = os.path.join(temp_path, "temp_locations.json")
    if os.path.exists(temp_locations_file):
        os.remove(temp_locations_file)
    temp_items_file = os.path.join(temp_path, "temp_items.json")
    if os.path.exists(temp_items_file):
        os.remove(temp_items_file)