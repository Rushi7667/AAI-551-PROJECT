"""
Calorie calculator module for the Fitness Tracker.
"""
import streamlit as st


def show_calorie_calculator():
    """
    Display a calorie calculator in Streamlit.
    Allows users to calculate daily caloric needs based on various factors.
    """
    st.title("🔢 Calorie Calculator")
    
    st.markdown("""
    This calculator helps estimate your daily caloric needs based on the **Harris-Benedict equation**.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
        gender = st.radio("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=70.0)
    
    with col2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=170.0)
        activity = st.selectbox(
            "Activity Level",
            ["Sedentary (little or no exercise)", 
             "Lightly active (1-3 days/week)",
             "Moderately active (3-5 days/week)",
             "Very active (6-7 days/week)",
             "Extremely active (physical job)"]
        )
    
    # Calculate BMR (Basal Metabolic Rate) using Harris-Benedict equation
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    # Activity multipliers
    activity_multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Extremely active (physical job)": 1.9
    }
    
    tdee = bmr * activity_multipliers[activity]
    
    st.divider()
    
    col_result1, col_result2 = st.columns(2)
    
    with col_result1:
        st.metric("Basal Metabolic Rate (BMR)", f"{bmr:.0f} kcal/day")
    
    with col_result2:
        st.metric("Total Daily Energy Expenditure (TDEE)", f"{tdee:.0f} kcal/day")
    
    st.info(f"""
    **Your Results:**
    - To **lose weight**: Consume ~{tdee - 500:.0f} kcal/day (500 kcal deficit)
    - To **maintain weight**: Consume ~{tdee:.0f} kcal/day
    - To **gain weight**: Consume ~{tdee + 500:.0f} kcal/day (500 kcal surplus)
    """)
