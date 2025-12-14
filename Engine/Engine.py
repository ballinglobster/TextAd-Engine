
import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext, Menu
import webbrowser
import subprocess
import sv_ttk
import ttkbootstrap as ttk
import json


class Engine:
    # Initialize the engine
    def __init__(self, root):
        self.root = root
        self.root.title("TextAd Engine")
        # self.root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
        self.current_game_path = None
        self.unsaved_changes = False

        self.create_main_menu()
        self.create_main_interface()

        self.template_path = os.path.join(os.path.dirname(__file__), "TemplateFiles", "Game")
        self.temp_path = os.path.join(os.path.dirname(__file__), "TempFiles")
        
    # Create main menu
    def create_main_menu(self):
        # Window size
        self.root.geometry("400x300")
        # menubar = Menu(self.root)
        # filemenu = Menu(menubar, tearoff=0)
        # filemenu.add_command(label="New Game", command=self.new_game)
        # filemenu.add_command(label="Open Game", command=self.open_game)
        # filemenu.add_separator()
        # filemenu.add_command(label="Exit", command=self.root.quit)
        # menubar.add_cascade(label="File", menu=filemenu)
        # self.root.config(menu=menubar)

    # Create main menu interface
    def create_main_interface(self):
        self.reset_grid_weights(self.root)
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Grid weight configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = ttk.Label(self.main_frame, text="TextAd Engine", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, padx=10, pady=10)

        # Buttons for New Game, Open Game, Quit (all same size, scalable)
        new_game_button = ttk.Button(self.main_frame, text="New Game", command=self.new_game)
        new_game_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        open_game_button = ttk.Button(self.main_frame, text="Open Game", command=self.open_game)
        open_game_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        quit_button = ttk.Button(self.main_frame, text="Quit", command=self.root.quit)
        quit_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
    # If new game is clicked
    def new_game(self):
        game_name = simpledialog.askstring("New Game", "Enter the name of your new game:")
        if game_name:
            game_path = filedialog.askdirectory(title="Select Directory to Create New Game")
            if game_path:
                full_game_path = os.path.join(game_path, game_name)
                try:
                    shutil.copytree(self.template_path, full_game_path)
                    messagebox.showinfo("Success", f"New game '{game_name}' created successfully!")
                    self.current_game_path = full_game_path
                    self.unsaved_changes = False
                    self.open_game_editor()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create new game: {e}")

    # If open game is clicked
    def open_game(self):
        game_path = filedialog.askdirectory(title="Select Game Directory")
        if game_path:
            if os.path.exists(os.path.join(game_path, "index.html")) and \
                os.path.exists(os.path.join(game_path, "TextBasedAdventure.js")) and \
                os.path.exists(os.path.join(game_path, "stylesheet.css")):
                self.current_game_path = game_path
                self.unsaved_changes = False
                self.open_game_editor()
            else:
                messagebox.showerror("Error", "Selected directory does not contain a valid game.")
                
    # Opens the game editor window
    def open_game_editor(self):
        editor_window = self.root
        editor_window.title(f"Editing Game: {os.path.basename(self.current_game_path)}")

        self.editor_window = editor_window
        # Window size
        editor_window.geometry("800x600")
        editor_window.minsize(600, 400)

        # Editor protocol
        editor_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # close main window and make editor the main window
        self.switch_main_interface()


        self.create_game_editor_interface(self.root)

        self.check_for_temp_files()

    # Create game editor interface
    def create_game_editor_interface(self, parent):
        self.reset_grid_weights(parent)
        menu_frame = ttk.Frame(parent)
        menu_frame.grid(row=0, column=0, sticky="ew")
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.columnconfigure(1, weight=0)

        # Title with Background that spans the entire width
        title_label = ttk.Label(menu_frame, text="TextAd Engine - Game Editor", font=("Helvetica", 14), anchor="w")
        title_label.configure(background="#101010")
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

        # Left-side buttons
        left_frame = ttk.Frame(menu_frame)
        left_frame.grid(row=1, column=0, sticky="w")
        ttk.Button(left_frame, text="Home", command=self.go_back_to_main_menu, bootstyle="secondary").pack(side="left", padx=2, pady=2)
        ttk.Button(left_frame, text="Save Changes", command=self.save_game_changes, bootstyle="secondary").pack(side="left", padx=2, pady=2)
        ttk.Button(left_frame, text="Playtest Game", command=self.playtest_game, bootstyle="secondary").pack(side="left", padx=2, pady=2)

        # Right-side Help button
        ttk.Button(menu_frame, text="Help", command=self.go_to_help_page, bootstyle="secondary").grid(row=1, column=1, sticky="e", padx=2, pady=2)
        self.editor_frame = ttk.Frame(parent, padding="10")
        self.editor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Configure grid weights for scaling
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        for i in range(3):
            self.editor_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.editor_frame.grid_columnconfigure(i, weight=1)


        # Buttons for editing locations, items, objects, characters
        location_button = ttk.Button(self.editor_frame, text="Edit Locations", command=self.edit_locations)
        location_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        item_button = ttk.Button(self.editor_frame, text="Edit Items", command=self.edit_items)
        item_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        object_button = ttk.Button(self.editor_frame, text="Edit Objects", command=self.edit_objects)
        object_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        character_button = ttk.Button(self.editor_frame, text="Edit Characters", command=self.edit_characters)
        character_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    # Methods for editing game data
    def edit_locations(self):
        # Open location editor window
        # There will be a list of locations to choose from, and an option to add new locations
        # Inside the location editor, you can add location data:
        # image, description, items, objects, scenery, characters, choices, and linked locations
        # It will open a new window with all the location data editable
        Toplevel = tk.Toplevel(self.root)
        Toplevel.title("Edit Locations")
        Toplevel.geometry("600x400")

        self.location_editor_window = Toplevel

        # Left frame for location list
        # Button to add new location
        def add_location_and_refresh():
            new_location_id = simpledialog.askstring("New Location", "Enter the ID for the new location:")
            if new_location_id and new_location_id not in self.locations_data:
                self.add_another_location(
                    new_location_id,
                    {
                        "image": "",
                        "description": "",
                        "items": [],
                        "objects": [],
                        "scenery": [],
                        "characters": [],
                        "choices": [],
                        "connected-locations": {}
                    }
                )
                location_listbox.delete(0, tk.END)
                location_listbox.insert(tk.END, *self.locations_data.keys())

        # add_location_button = ttk.Button(Toplevel, text="Add New Location", command=lambda: self.add_another_location(
        #     simpledialog.askstring("New Location", "Enter the ID for the new location:"),
        #     {
        #         "image": "",
        #         "description": "",
        #         "items": [],
        #         "objects": [],
        #         "scenery": [],
        #         "characters": [],
        #         "choices": [],
        #         "locations": {}
        #     }
        # ))
        add_location_button = ttk.Button(Toplevel, text="Add New Location", command=add_location_and_refresh)
        add_location_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        left_frame = ttk.Frame(Toplevel, padding="10")
        left_frame.grid(row=1, column=0, sticky="ns")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        location_listbox = tk.Listbox(left_frame)
        location_listbox.grid(row=1, column=0, sticky="ns")
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=location_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        location_listbox.config(yscrollcommand=scrollbar.set)
        # Right frame for location details
        right_frame = ttk.Frame(Toplevel, padding="10")
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        location_details_text = scrolledtext.ScrolledText(right_frame)
        location_details_text.grid(row=1, column=0, sticky="nsew")

        # Load temporary location data if exists
        temp_file = os.path.join(self.temp_path, "temp_locations.json")
        if os.path.exists(temp_file):
            with open(temp_file, "r", encoding="utf-8") as f:
                self.locations_data = json.load(f)
                self.mark_unsaved_changes()
        else:
            self.locations_data = self.get_locations()
        # Load location data
        if self.locations_data:
            location_listbox.insert(tk.END, *self.locations_data.keys())
        else:
            location_listbox.insert(tk.END, "No locations found.")

        # Function to display location details when selected
        def show_location_details(event):
            selection = location_listbox.curselection()
            if not selection:
                return

            location_name = location_listbox.get(selection[0])
            location_details = self.get_location_details(location_name)

            for widget in right_frame.winfo_children():
                widget.destroy()

            if not location_details:
                ttk.Label(right_frame, text="No details found for this location.").grid(row=0, column=0, sticky="nsew")
                return

            row = 0
            for key, value in location_details.items():
                ttk.Label(right_frame, text=f"{key}:", font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="w", pady=2)
                if isinstance(value, list):
                    # Show list as a comma-separated string in an Entry
                    entry = ttk.Entry(right_frame, width=40)
                    entry.insert(0, ", ".join(str(item) for item in value))
                    entry.grid(row=row, column=1, sticky="w", padx=2)
                elif isinstance(value, dict):
                    # Show dict as a string in an Entry (e.g., key1: value1, key2: value2)
                    entry = ttk.Entry(right_frame, width=40)
                    entry.insert(0, ", ".join(f"{k}: {v}" for k, v in value.items()))
                    entry.grid(row=row, column=1, sticky="w", padx=2)
                else:
                    entry = ttk.Entry(right_frame, width=40)
                    entry.insert(0, str(value))
                    entry.grid(row=row, column=1, sticky="w", padx=2)
                row += 1

        location_listbox.bind("<<ListboxSelect>>", show_location_details)

    def edit_items(self):
        Toplevel = tk.Toplevel(self.root)
        Toplevel.title("Edit Items")
        Toplevel.geometry("600x400")

        self.item_editor_window = Toplevel

        def add_item_and_refresh():
            new_item_id = simpledialog.askstring("New Item", "Enter the ID for the new item:")
            if new_item_id and new_item_id not in self.items_data:
                self.add_another_item(
                    new_item_id,
                    {
                        "name": "",
                        "description": "",
                        "location": "",
                        "properties": {}
                    }
                )
                item_listbox.delete(0, tk.END)
                item_listbox.insert(tk.END, *self.items_data.keys())

        add_item_button = ttk.Button(Toplevel, text="Add New Item", command=add_item_and_refresh)
        add_item_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        left_frame = ttk.Frame(Toplevel, padding="10")
        left_frame.grid(row=1, column=0, sticky="ns")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        item_listbox = tk.Listbox(left_frame)
        item_listbox.grid(row=1, column=0, sticky="ns")
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=item_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        item_listbox.config(yscrollcommand=scrollbar.set)
        # Right frame for item details
        right_frame = ttk.Frame(Toplevel, padding="10")
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        item_details_text = scrolledtext.ScrolledText(right_frame)
        item_details_text.grid(row=1, column=0, sticky="nsew")

        # Load temporary item data if exists
        temp_file = os.path.join(self.temp_path, "temp_items.json")
        if os.path.exists(temp_file):
            with open(temp_file, "r", encoding="utf-8") as f:
                self.items_data = json.load(f)
                self.mark_unsaved_changes()
        else:
            self.items_data = self.get_items()
        # Load item data
        if self.items_data:
            item_listbox.insert(tk.END, *self.items_data.keys())
        else:
            item_listbox.insert(tk.END, "No items found.")

        # Function to display item details when selected
        def show_item_details(event):
            selection = item_listbox.curselection()
            if not selection:
                return

            item_name = item_listbox.get(selection[0])
            item_details = self.get_item_details(item_name)

            for widget in right_frame.winfo_children():
                widget.destroy()

            if not item_details:
                ttk.Label(right_frame, text="No details found for this item.").grid(row=0, column=0, sticky="nsew")
                return

            row = 0
            for key, value in item_details.items():
                ttk.Label(right_frame, text=f"{key}:", font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="w", pady=2)
                if isinstance(value, dict):
                    entry = ttk.Entry(right_frame, width=40)
                    entry.insert(0, ", ".join(f"{k}: {v}" for k, v in value.items()))
                    entry.grid(row=row, column=1, sticky="w", padx=2)
                else:
                    entry = ttk.Entry(right_frame, width=40)
                    entry.insert(0, str(value))
                    entry.grid(row=row, column=1, sticky="w", padx=2)
                row += 1
        item_listbox.bind("<<ListboxSelect>>", show_item_details)


    def edit_objects(self):
        messagebox.showinfo("Edit Objects", "Object editing interface to be implemented.")

    def edit_characters(self):
        messagebox.showinfo("Edit Characters", "Character editing interface to be implemented.")

    # Location data handling methods
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
        self.save_temp_locations()

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

    # Item data handling methods
    def get_items(self):
        js_file_path = os.path.join(self.current_game_path, "TextBasedAdventure.js")
        if not os.path.exists(js_file_path):
            messagebox.showerror("Error", "TextBasedAdventure.js file not found.")
            return None
        
        with open(js_file_path, "r", encoding="utf-8") as js_file:
            js_content = js_file.read()

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
            items = game_data.get("items", {})
            return items
        except Exception as e:
            messagebox.showerror("Error", f"Could not parse gameData: {e}")
            return None

    def get_item_details(self, item_id):
        if hasattr(self, "items_data") and self.items_data and item_id in self.items_data:
            return self.items_data[item_id]
        else:
            messagebox.showerror("Error", f"Item '{item_id}' not found.")
            return None
        
    def add_another_item(self, item_id, item_data):
        if not hasattr(self, "items_data") or self.items_data is None:
            self.items_data = {}
        self.items_data[item_id] = item_data
        self.mark_unsaved_changes()
        self.save_temp_items()

    def save_items(self, items):
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

        # Update items
        game_data["items"] = items

        # Dump back to JS object string
        new_game_data_str = json.dumps(game_data, indent=4)

        # Rebuild the JS file
        new_js_content = js_content[:match.start(2)] + new_game_data_str + js_content[match.end(2):]

        with open(js_file_path, "w", encoding="utf-8") as js_file:
            js_file.write(new_js_content)

    # Save game changes
    def save_game_changes(self):
        self.save_locations(self.locations_data)
        self.save_items(self.items_data)
        # Remove temporary files after saving
        temp_locations_file = os.path.join(self.temp_path, "temp_locations.json")
        if os.path.exists(temp_locations_file):
            os.remove(temp_locations_file)
        temp_items_file = os.path.join(self.temp_path, "temp_items.json")
        if os.path.exists(temp_items_file):
            os.remove(temp_items_file)

        self.unsaved_changes = False
        messagebox.showinfo("Save", "Game changes saved successfully!")
        if hasattr(self, "location_editor_window") and self.location_editor_window.winfo_exists():
            title = self.location_editor_window.title()
            if "*" in title:
                self.location_editor_window.title(title.replace(" * (Unsaved Changes)", ""))
        
        if hasattr(self, "editor_window") and self.editor_window.winfo_exists():
            title = self.editor_window.title()
            if "*" in title:
                self.editor_window.title(title.replace(" * (Unsaved Changes)", ""))
        
    # Playtest the game
    def playtest_game(self):
        if self.current_game_path:
            index_file = os.path.join(self.current_game_path, "index.html")
            webbrowser.open_new_tab(f"file://{index_file}")
        else:
            messagebox.showerror("Error", "No game is currently open for playtesting.")

    def go_back_to_main_menu(self):
        if self.check_unsaved_changes():
            self.switch_main_interface()
            self.create_main_interface()

    def go_to_help_page(self):
        help_url = "https://thelobster.dev"
        webbrowser.open_new_tab(help_url)

    # Check for unsaved changes before closing or opening another game
    def check_unsaved_changes(self):
        if self.unsaved_changes:
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
            if response:  # Yes
                self.save_game_changes()
                return True
            elif response is False:  # No
                temp_locations_file = os.path.join(self.temp_path, "temp_locations.json")
                if os.path.exists(temp_locations_file):
                    os.remove(temp_locations_file)
                temp_items_file = os.path.join(self.temp_path, "temp_items.json")
                if os.path.exists(temp_items_file):
                    os.remove(temp_items_file)
                return True
            else:  # Cancel
                return False
        return True
    
    def mark_unsaved_changes(self):
        self.unsaved_changes = True

        if hasattr(self, "location_editor_window") and self.location_editor_window.winfo_exists():
            title = self.location_editor_window.title()
            if "*" not in title:
                self.location_editor_window.title(title + " * (Unsaved Changes)")
        
        if hasattr(self, "editor_window") and self.editor_window.winfo_exists():
            title = self.editor_window.title()
            if "*" not in title:
                self.editor_window.title(title + " * (Unsaved Changes)")

        if hasattr(self, "item_editor_window") and self.item_editor_window.winfo_exists():
            title = self.item_editor_window.title()
            if "*" not in title:
                self.item_editor_window.title(title + " * (Unsaved Changes)")

    def check_if_unsaved(self):
        return self.unsaved_changes
    
    # Handle application exit (give chance to save unsaved changes)
    def on_exit(self):
        if self.unsaved_changes:
            # Only show the save changes dialog
            if not self.check_unsaved_changes():
                return  # User cancelled or closed the dialog
            # If user chose to save or not save, just quit
            self.root.destroy()
        else:
            # No unsaved changes, ask for quit confirmation
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()

    def switch_main_interface(self):
        # Destroy current main frame if it exists
        if hasattr(self, "main_frame") and self.main_frame.winfo_exists():
            self.main_frame.destroy()
        # Destroy editor frame if it exists
        if hasattr(self, "editor_frame") and self.editor_frame.winfo_exists():
            self.editor_frame.destroy()

    def reset_grid_weights(self, parent):
        for i in range(parent.grid_size()[1]):
            parent.grid_rowconfigure(i, weight=0)
        for i in range(parent.grid_size()[0]):
            parent.grid_columnconfigure(i, weight=0)


    # Check if there are temporary files, then ask player whether to load
    # If yes, load temp files
    # Else, delete temp files
    def check_for_temp_files(self):
        temp_locations_file = os.path.join(self.temp_path, "temp_locations.json")
        temp_items_file = os.path.join(self.temp_path, "temp_items.json")
        temp_files_exist = os.path.exists(temp_locations_file) or os.path.exists(temp_items_file)

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


    # TEMPORARY SAVING FUNCTIONS    
    def save_temp_locations(self):
        temp_file = os.path.join(self.temp_path, "temp_locations.json")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(self.locations_data, f, indent=4)
    
    def save_temp_items(self):
        temp_file = os.path.join(self.temp_path, "temp_items.json")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(self.items_data, f, indent=4)

    # CLEAR TEMP FILES  
    def clear_temp_files(self):
        temp_locations_file = os.path.join(self.temp_path, "temp_locations.json")
        if os.path.exists(temp_locations_file):
            os.remove(temp_locations_file)
        temp_items_file = os.path.join(self.temp_path, "temp_items.json")
        if os.path.exists(temp_items_file):
            os.remove(temp_items_file)
    
# Run the engine
if __name__ == "__main__":
    root = ttk.Window(themename="textadengine")
    engine = Engine(root)
    root.protocol("WM_DELETE_WINDOW", engine.on_exit)
    root.mainloop()