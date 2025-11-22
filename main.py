# Author: Linpeng Mao
# Date: 11/18/2025
# Description: Entry point of the Fitness Tracker application.
#              Initializes the main Tkinter window, ensures required directories,
#              and launches the login interface provided by auth.py.

# main.py

import tkinter as tk
import os
from auth import login_screen

DATA_DIR = "data"
REFERENCE_DIR = "reference"

def ensure_directories():
    """Ensure required directories exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REFERENCE_DIR, exist_ok=True)

def center_window(win, width=400, height=300):
    """Center the window on the screen"""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def main():
    ensure_directories()

    root = tk.Tk()
    root.title("Fitness Tracker")
    center_window(root, 500, 380)
    root.resizable(False, False)

    # Load login screen
    login_screen(root)

    root.mainloop()

if __name__ == "__main__":
    main()
