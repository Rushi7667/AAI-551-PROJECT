import os
import csv
from datetime import datetime

DATA_DIR = "data"


def today_str():
   
    return datetime.now().strftime("%Y-%m-%d")


def get_user_data_path(username: str) -> str:
#    Return the path for the user's main tracking CSV file
    
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f"{username}_tracker.csv"
    return os.path.join(DATA_DIR, filename)


def ensure_data_file(username: str):
#    Ensure the user's main tracking CSV exists and contains
    
    path = get_user_data_path(username)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "in_cal", "out_cal", "goal"])
    return path


def get_nutrition_data_path(username: str) -> str:
#    Return the file path for the user's nutrition records.

    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{username}_nutrition.csv")


def get_exercise_data_path(username: str) -> str:
    
  #  Return the path for the exercise log file.

    
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, "exercise_log.csv")
