"""
generate_sample_logs.py
Creates sample nutrition and exercise logs using the project's backend functions.
"""
import os
import random
from datetime import date, timedelta
import pandas as pd

import nutrition
import exercise

USERNAME = "Rushi"
NUM_ENTRIES = 20

# Helper: random date within last `days_back` days
def random_recent_date(days_back=30):
    today = date.today()
    delta_days = random.randint(0, days_back - 1)
    return (today - timedelta(days=delta_days)).isoformat()


def generate_nutrition_logs(username=USERNAME, n=NUM_ENTRIES):
    # Ensure data dir exists
    os.makedirs(nutrition.DATA_DIR, exist_ok=True)
    user_file = os.path.join(nutrition.DATA_DIR, f"{username}_nutrition.csv")

    # Remove existing file so we start fresh for this run
    if os.path.exists(user_file):
        os.remove(user_file)
        print(f"Removed existing file: {user_file}")

    food_df = nutrition.load_food_data()
    if food_df.empty:
        raise SystemExit("Food dataset not found or could not be loaded. Aborting nutrition log generation.")

    food_list = food_df['Food'].dropna().unique().tolist()
    for i in range(n):
        d = random_recent_date(30)
        food = random.choice(food_list)
        weight_g = round(random.uniform(50, 400), 1)
        cals = nutrition.calculate_calories(food, weight_g, food_df)
        nutrition.save_user_record(username, d, food, weight_g, cals)
    print(f"Wrote {n} nutrition entries to {user_file}")


def generate_exercise_logs(n=NUM_ENTRIES):
    # Ensure data dir exists
    os.makedirs(os.path.dirname(exercise.EXERCISE_LOG_PATH) or 'data', exist_ok=True)

    # Remove existing exercise log to start fresh
    if os.path.exists(exercise.EXERCISE_LOG_PATH):
        os.remove(exercise.EXERCISE_LOG_PATH)
        print(f"Removed existing file: {exercise.EXERCISE_LOG_PATH}")

    activities = exercise.get_activity_list()
    if not activities:
        raise SystemExit("Exercise dataset not found or no activities available. Aborting exercise log generation.")

    for i in range(n):
        d = random_recent_date(30)
        activity = random.choice(activities)
        duration = random.randint(20, 90)  # minutes
        weight_kg = round(random.uniform(60, 90), 1)
        cals = exercise.calculate_calories(activity, weight_kg, duration)
        exercise.save_exercise_entry(d, activity, duration, weight_kg, cals)
    print(f"Wrote {n} exercise entries to {exercise.EXERCISE_LOG_PATH}")


def show_head_tail(path, label, n=5):
    if not os.path.exists(path):
        print(f"{label}: file not found: {path}")
        return
    df = pd.read_csv(path)
    print(f"\n=== {label} : HEAD ({n}) ===")
    print(df.head(n).to_string(index=False))
    print(f"\n=== {label} : TAIL ({n}) ===")
    print(df.tail(n).to_string(index=False))


if __name__ == "__main__":
    print("Starting sample log generation...")

    # 1. Nutrition
    generate_nutrition_logs(USERNAME, NUM_ENTRIES)

    # 2. Exercise
    generate_exercise_logs(NUM_ENTRIES)

    # 3. Show results
    nutrition_path = os.path.join(nutrition.DATA_DIR, f"{USERNAME}_nutrition.csv")
    exercise_path = exercise.EXERCISE_LOG_PATH

    show_head_tail(nutrition_path, f"Nutrition ({USERNAME})")
    show_head_tail(exercise_path, "Exercise Log")

    print("Sample log generation complete.")
