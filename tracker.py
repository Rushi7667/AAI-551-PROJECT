# ------------------------------------------------------------
# Author: Linpeng Mao
# Description: Tracking module for nutrition and exercise logging.
# ------------------------------------------------------------

import streamlit as st
from datetime import date
import storage

NUTRI_FILE = "nutrition.json"
EXER_FILE = "exercise.json"


# ---------------- Utility Functions ----------------

def _load(file, default):
    """Load JSON data from storage."""
    return storage.load_json(file, default)


def _save(file, obj):
    """Save JSON data to storage."""
    storage.save_json(file, obj)


# ---------------- Nutrition Tracking ----------------

def log_nutrition(user):
    """Page for logging food intake."""
    st.title("🍎 Log Nutrition")

    col1, col2 = st.columns(2)
    
    with col1:
        food = st.text_input("Food Name")
        calories = st.number_input("Calories", min_value=0, step=1)
    
    with col2:
        dt = st.date_input("Date", value=date.today())
        weight_g = st.number_input("Weight (grams)", min_value=1, step=10, value=100)

    if st.button("Add Nutrition Record"):
        if not food:
            st.error("Please enter a food name.")
        else:
            raw = _load(NUTRI_FILE, {})
            raw.setdefault(user, []).append({
                "date": dt.isoformat(),
                "food": food,
                "weight_g": weight_g,
                "calories": calories
            })
            _save(NUTRI_FILE, raw)
            st.success(f"✅ Added: {weight_g}g of {food} ({calories} kcal)")

    st.divider()
    st.subheader("📋 Nutrition History")
    
    raw = _load(NUTRI_FILE, {})
    user_records = raw.get(user, [])
    
    if user_records:
        import pandas as pd
        df = pd.DataFrame(user_records)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total_cals = df['calories'].sum()
        avg_cals = df['calories'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calories", f"{total_cals:.0f} kcal")
        with col2:
            st.metric("Avg per Entry", f"{avg_cals:.0f} kcal")
        with col3:
            st.metric("Total Entries", len(df))


# ---------------- Exercise Tracking ----------------

def log_exercise(user):
    """Page for logging exercise activities."""
    st.title("💪 Log Exercise")

    col1, col2 = st.columns(2)
    
    with col1:
        ex_name = st.text_input("Exercise Name")
        duration = st.number_input("Duration (minutes)", min_value=1, step=5, value=30)
    
    with col2:
        burnt = st.number_input("Calories Burned", min_value=0, step=1)
        dt = st.date_input("Date", value=date.today())

    if st.button("Add Exercise Record"):
        if not ex_name:
            st.error("Please enter an exercise name.")
        else:
            raw = _load(EXER_FILE, {})
            raw.setdefault(user, []).append({
                "date": dt.isoformat(),
                "exercise": ex_name,
                "duration_min": duration,
                "calories_burned": burnt
            })
            _save(EXER_FILE, raw)
            st.success(f"✅ Added: {ex_name} for {duration} minutes ({burnt} kcal burned)")

    st.divider()
    st.subheader("📋 Exercise History")
    
    raw = _load(EXER_FILE, {})
    user_records = raw.get(user, [])
    
    if user_records:
        import pandas as pd
        df = pd.DataFrame(user_records)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total_burnt = df['calories_burned'].sum()
        total_duration = df['duration_min'].sum()
        avg_burnt = df['calories_burned'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calories Burned", f"{total_burnt:.0f} kcal")
        with col2:
            st.metric("Total Duration", f"{total_duration:.0f} min")
        with col3:
            st.metric("Avg Burnt per Session", f"{avg_burnt:.0f} kcal")
