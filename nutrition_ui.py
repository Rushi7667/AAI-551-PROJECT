#Author : Ishaan Dange
#Description : Streamlit interface allowing users to select food, input weight, and visualize daily logs.

import streamlit as st
import pandas as pd
from datetime import date
import nutrition

def app(username="Ishaan"):
    # --- sidebar for professional look ---
    st.sidebar.header(f"User: {username}")
    st.sidebar.info("Track your daily caloric intake efficiently.")
    
    st.title("🍎 Nutrition Tracker")
    st.markdown("### Log your daily meals")

    # 1. Load Data safely
    food_df = nutrition.load_food_data()
    
    if food_df.empty:
        st.error("⚠️ Critical Error: Food database not found.")
        st.warning("Please ensure 'Food and Calories.csv' is inside the 'food' folder.")
        return

    # 2. The Input Form
    with st.form("nutrition_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date_input = st.date_input("Date", date.today())
            # Sort the list so it's easier to find items
            food_list = sorted(food_df['Food'].unique().tolist())
            food_select = st.selectbox("Select Food Item", food_list)
        
        with col2:
            weight_input = st.number_input("Weight (grams)", min_value=1.0, value=100.0, step=10.0)
        
        # Calculate preview
        estimated_cals = nutrition.calculate_calories(food_select, weight_input, food_df)
        st.info(f"⚡ Estimated Energy: **{estimated_cals} kcal**")
        
        # Submit Button
        submitted = st.form_submit_button("Add to Log")

        if submitted:
            success = nutrition.save_user_record(username, date_input, food_select, weight_input, estimated_cals)
            if success:
                st.success(f"✅ Logged: {weight_input}g of {food_select}")
            else:
                st.error("❌ Failed to save data.")

    # 3. History Section (Required for Member C to visualize)
    st.divider()
    st.subheader("📅 Your Recent Logs")
    
    # Construct path safely using the backend variable
    user_file_path = f"data/{username}_nutrition.csv"
    
    try:
        # Check if file exists using os first to avoid crashing
        import os
        if os.path.exists(os.path.join(nutrition.DATA_DIR, f"{username}_nutrition.csv")):
            # Read the file safely
            full_path = os.path.join(nutrition.DATA_DIR, f"{username}_nutrition.csv")
            history_df = pd.read_csv(full_path)
            
            # Show last 5 entries
            st.dataframe(history_df.tail(5), use_container_width=True)
            
            # Show a quick total stats for fun
            total_cals = history_df['Calories'].sum()
            st.metric("Total Calories Tracked (All Time)", f"{round(total_cals, 2)} kcal")
        else:
            st.info("No logs found yet. Add your first meal above!")
            
    except Exception as e:
        st.error(f"Could not load history: {e}")

if __name__ == "__main__":
    app()
