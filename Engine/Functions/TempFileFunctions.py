import os
import json
from tkinter import messagebox

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

def save_temp_objects(objects_data, temp_path):
    temp_file = os.path.join(temp_path, "temp_objects.json")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(objects_data, f, indent=4)

# CLEAR TEMP FILES  
def clear_temp_files(temp_path):
    temp_locations_file = os.path.join(temp_path, "temp_locations.json")
    if os.path.exists(temp_locations_file):
        os.remove(temp_locations_file)
    temp_items_file = os.path.join(temp_path, "temp_items.json")
    if os.path.exists(temp_items_file):
        os.remove(temp_items_file)

# Check for temp files and prompt user
def check_for_temp_files(self):
        temp_locations_file = os.path.join(self.temp_path, "temp_locations.json")
        temp_items_file = os.path.join(self.temp_path, "temp_items.json")
        temp_characters_file = os.path.join(self.temp_path, "temp_characters.json")
        temp_files_exist = os.path.exists(temp_locations_file) or os.path.exists(temp_items_file) or os.path.exists(temp_characters_file)

        if temp_files_exist:
            response = messagebox.askyesno("Load Backup Data", "Your previous session was not closed properly. Do you want to load the backup data?")
            if response:  # Yes
                if os.path.exists(temp_locations_file):
                    with open(temp_locations_file, "r", encoding="utf-8") as f:
                        self.locations_data = json.load(f)
                        self.mark_unsaved_changes()
                if os.path.exists(temp_items_file):
                    with open(temp_items_file, "r", encoding="utf-8") as f:
                        self.items_data = json.load(f)
                        self.mark_unsaved_changes()
            else:  # No
                if os.path.exists(temp_locations_file):
                    os.remove(temp_locations_file)
                if os.path.exists(temp_items_file):
                    os.remove(temp_items_file)
                if os.path.exists(temp_characters_file):
                    os.remove(temp_characters_file)