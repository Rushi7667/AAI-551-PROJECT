# Author: Linpeng Mao
# Date: 11/18/2025
# Description:
#   Handles user authentication logic for the Fitness Tracker app.
#   Provides GUI for login and registration, verifies user credentials,
#   and stores user data securely in users.csv (with hashed passwords).
#
# Functions:
#   - login_screen(root): Displays login and registration UI
#   - register_user(username, password): Registers new users
#   - validate_user(username, password): Validates login credentials

import tkinter as tk
from tkinter import messagebox
import csv
import os
import hashlib

USER_FILE = 'users.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password'])

    with open(USER_FILE, 'r') as f:
        reader = csv.reader(f)
        users = list(reader)

    for row in users:
        if row and row[0] == username:
            messagebox.showerror("Registration Failed", "Username already exists.")
            return

    with open(USER_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hash_password(password)])
    messagebox.showinfo("Success", "Registration successful!")

def validate_user(username, password):
    if not os.path.exists(USER_FILE):
        return False
    hashed = hash_password(password)
    with open(USER_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == username and row[1] == hashed:
                return True
    return False

def login_screen(root):
    from tracker import tracker_screen

    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, padx=30, pady=30)
    frame.pack(expand=True)

    tk.Label(frame, text="Welcome to Fitness Tracker", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tk.Label(frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, sticky='e', pady=5)
    username_entry = tk.Entry(frame, font=("Helvetica", 12), width=25)
    username_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, sticky='e', pady=5)
    password_entry = tk.Entry(frame, font=("Helvetica", 12), show="*", width=25)
    password_entry.grid(row=2, column=1, pady=5)

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if validate_user(username, password):
            tracker_screen(root, username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def attempt_register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username and password:
            register_user(username, password)
        else:
            messagebox.showwarning("Invalid Input", "Username and password cannot be empty.")

    login_btn = tk.Button(frame, text="Login", font=("Helvetica", 11), bg="#4CAF50", fg="white", width=15, command=attempt_login)
    login_btn.grid(row=3, column=0, pady=20)

    register_btn = tk.Button(frame, text="Register", font=("Helvetica", 11), bg="#2196F3", fg="white", width=15, command=attempt_register)
    register_btn.grid(row=3, column=1, pady=20)
