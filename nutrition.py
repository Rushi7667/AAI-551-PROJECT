# Author: Ishaan
# Description: Nutrition logic that loads food data, calculates calories, and saves user log

import pandas as pd
import os

# --- CONFIGURATION ---
DATA_DIR = 'data/'
FOOD_FOLDER = 'food'

def get_food_file_path():
    """
    Automatically finds the first CSV file in the 'food' folder.
    """
    if not os.path.exists(FOOD_FOLDER):
        return None
    
    # List all files and find the one ending in .csv
    files = os.listdir(FOOD_FOLDER)
    csv_files = [f for f in files if f.lower().endswith('.csv')]
    
    if not csv_files:
        return None
    
    # Return full path to that file
    return os.path.join(FOOD_FOLDER, csv_files[0])

def load_food_data():
    """
    Loads the food data using the automatically found file.
    """
    csv_path = get_food_file_path()
    if csv_path is None:
        return pd.DataFrame()

    try:
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def calculate_calories(food_name, weight_grams, food_df):
    food_item = food_df[food_df['Food'] == food_name]
    if not food_item.empty:
        cal_per_100 = float(food_item['Calories_per_100g'].values[0])
        return round((cal_per_100 / 100) * weight_grams, 2)
    return 0

def save_user_record(username, date, food, weight, calories):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    user_file = os.path.join(DATA_DIR, f"{username}_nutrition.csv")
    
    new_record = {
        'Date': [date],
        'Food': [food],
        'Weight_g': [weight],
        'Calories': [calories]
    }
    new_df = pd.DataFrame(new_record)

    if os.path.exists(user_file):
        new_df.to_csv(user_file, mode='a', header=False, index=False)
    else:
        new_df.to_csv(user_file, mode='w', header=True, index=False)
    
    return True
