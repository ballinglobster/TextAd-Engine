
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext, Menu
import webbrowser
import subprocess
import sv_ttk
import ttkbootstrap as ttk


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

        # Window size
        editor_window.geometry("800x600")
        editor_window.minsize(600, 400)

        # Editor protocol
        editor_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        # close main window and make editor the main window
        self.switch_main_interface()


        self.create_game_editor_interface(self.root)

    # Create game editor interface
    def create_game_editor_interface(self, parent):
        self.reset_grid_weights(parent)
        menu_frame = ttk.Frame(parent)
        menu_frame.grid(row=0, column=0, sticky="ew")
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.columnconfigure(1, weight=0)

        # Left-side buttons
        left_frame = ttk.Frame(menu_frame)
        left_frame.grid(row=0, column=0, sticky="w")
        ttk.Button(left_frame, text="Home", command=self.go_back_to_main_menu, bootstyle="secondary").pack(side="left", padx=2, pady=2)
        ttk.Button(left_frame, text="Save Changes", command=self.save_game_changes, bootstyle="secondary").pack(side="left", padx=2, pady=2)
        ttk.Button(left_frame, text="Playtest Game", command=self.playtest_game, bootstyle="secondary").pack(side="left", padx=2, pady=2)

        # Right-side Help button
        ttk.Button(menu_frame, text="Help", command=self.go_to_help_page, bootstyle="secondary").grid(row=0, column=1, sticky="e", padx=2, pady=2)
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
        messagebox.showinfo("Edit Locations", "Location editing interface to be implemented.")
        self.mark_unsaved_changes()

    def edit_items(self):
        messagebox.showinfo("Edit Items", "Item editing interface to be implemented.")

    def edit_objects(self):
        messagebox.showinfo("Edit Objects", "Object editing interface to be implemented.")

    def edit_characters(self):
        messagebox.showinfo("Edit Characters", "Character editing interface to be implemented.")

    # Save game changes
    def save_game_changes(self):
        self.unsaved_changes = False
        messagebox.showinfo("Save", "Game changes saved successfully!")
        
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
                return True
            else:  # Cancel
                return False
        return True
    
    def mark_unsaved_changes(self):
        self.unsaved_changes = True

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

# Run the engine
if __name__ == "__main__":
    root = ttk.Window(themename="textadengine")
    engine = Engine(root)
    root.protocol("WM_DELETE_WINDOW", engine.on_exit)
    root.mainloop()