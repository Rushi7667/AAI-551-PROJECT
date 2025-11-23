# Author: Rushi
# Improved Exercise UI with Recent Logs, Sidebar, Form Layout, and User Stats

import streamlit as st
from datetime import date
import pandas as pd
import os
import exercise


def app(username="Rushi"):
    # --- Sidebar ---
    st.sidebar.header(f"User: {username}")
    st.sidebar.info("Track your workouts and calories burned throughout the day!")

    # --- Main Title ---
    st.title("🏋️ Exercise Tracker")
    st.markdown("### Log your workouts and monitor your performance")

    # Load activities
    try:
        activities = exercise.get_activity_list()
    except Exception:
        st.error("⚠ Exercise dataset missing or unreadable. Please check `execersice/` folder.")
        return

    # ---- Input Form ----
    with st.form("exercise_form"):
        col1, col2 = st.columns(2)

        with col1:
            user_date = st.date_input("📆 Select Date", value=date.today())
            selected_activity = st.selectbox("🏃 Select Exercise Activity", activities)

        with col2:
            duration = st.number_input(
                "⏱ Duration (minutes)",
                min_value=1,
                max_value=300,
                value=30
            )
            weight_kg = st.number_input(
                "⚖ Enter Your Weight (kg)",
                min_value=20.0,
                max_value=200.0,
                value=70.0
            )

        # Live Calculator Preview
        try:
            preview_cals = exercise.calculate_calories(
                activity=selected_activity,
                weight_kg=weight_kg,
                duration_minutes=duration
            )
            st.info(f"🔥 Estimated Calories Burned: **{preview_cals} kcal**")
        except:
            st.warning("Unable to calculate preview calories.")

        submitted = st.form_submit_button("Add Workout")

        if submitted:
            try:
                calories = preview_cals

                # Save entry
                exercise.save_exercise_entry(
                    date=str(user_date),
                    activity=selected_activity,
                    duration_minutes=duration,
                    weight_kg=weight_kg,
                    calories_burned=calories
                )

                st.success(f"✅ Workout Logged: {selected_activity} for {duration} min")
            except Exception as e:
                st.error(f"❌ Failed to save entry: {e}")

    # ---- Recent Logs Section ----
    st.divider()
    st.subheader("📅 Your Recent Exercise Logs")

    exercise_file = "data/exercise_log.csv"

    if os.path.exists(exercise_file):
        try:
            history_df = pd.read_csv(exercise_file)

            # Show last 5 logs
            st.dataframe(history_df.tail(5), use_container_width=True)

            # Quick Statistics
            total_burned = history_df["calories_burned"].sum()
            last_activity = history_df.tail(1)["exercise_type"].values[0]

            c1, c2 = st.columns(2)
            c1.metric("🔥 Total Calories Burned", f"{round(total_burned, 2)} kcal")
            c2.metric("🏃 Last Activity", last_activity)

        except Exception as e:
            st.error(f"⚠ Error loading exercise history: {e}")

    else:
        st.info("No exercise logs found yet. Start logging your workouts above!")


if __name__ == "__main__":
    app()