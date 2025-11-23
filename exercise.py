# Author: Rushi
# Description: Exercise module that loads exercise dataset, calculates calories burned
#               using calories-per-kg method, and saves user exercise logs.

import os
import pandas as pd

DATASET_PATH = "exercise/exercise_dataset.csv"

EXERCISE_LOG_PATH = "data/exercise_log.csv"


def load_exercise_dataset():
   
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    return df


def get_activity_list():
    df = load_exercise_dataset()
    return df["Activity, Exercise or Sport (1 hour)"].tolist()


def calculate_calories(activity, weight_kg, duration_minutes):
 
    df = load_exercise_dataset()

    row = df[df["Activity, Exercise or Sport (1 hour)"] == activity]

    if row.empty:
        raise ValueError("Activity not found in dataset")

    calories_per_kg = float(row["Calories per kg"].values[0])

    calories_burned = calories_per_kg * weight_kg * (duration_minutes / 60)

    return round(calories_burned, 2)


def save_exercise_entry(date, activity, duration_minutes, weight_kg, calories_burned):
   

    entry = {
        "date": [date],
        "exercise_type": [activity],
        "duration_minutes": [duration_minutes],
        "user_weight_kg": [weight_kg],
        "calories_burned": [calories_burned],
    }

    df_new = pd.DataFrame(entry)

    os.makedirs("data", exist_ok=True)

    if os.path.exists(EXERCISE_LOG_PATH):
        df_existing = pd.read_csv(EXERCISE_LOG_PATH)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(EXERCISE_LOG_PATH, index=False)
    else:
        df_new.to_csv(EXERCISE_LOG_PATH, index=False)
