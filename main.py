# ------------------------------------------------------------
# Author: Linpeng Mao
# Description: Main Streamlit application for the Fitness Tracker.
# ------------------------------------------------------------

import streamlit as st
import auth
import tracker
import visualize
import calories

st.set_page_config(page_title="Fitness Tracker", layout="wide")

# Initialize session state for user login
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- LOGIN PAGE ----------------
def login_page():
    """Display login & registration page."""
    st.title("🏋️ Fitness Tracker - Login")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    # Login Tab
    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if auth.check_login(username, password):
                st.session_state.user = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    # Register Tab
    with register_tab:
        new_user = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type="password")
        if st.button("Register"):
            ok, msg = auth.register_user(new_user, new_pwd)
            if ok:
                st.success(msg)
            else:
                st.error(msg)


# ---------------- MAIN APP ----------------
def main_app():
    """Main user interface after login."""
    st.sidebar.title(f"Hello, {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Log Nutrition", "Log Exercise", "Calorie Calculator"]
    )

    if page == "Dashboard":
        visualize.show_dashboard(st.session_state.user)
    elif page == "Log Nutrition":
        tracker.log_nutrition(st.session_state.user)
    elif page == "Log Exercise":
        tracker.log_exercise(st.session_state.user)
    elif page == "Calorie Calculator":
        calories.show_calorie_calculator()


# ---------------- ENTRY ----------------
if st.session_state.user is None:
    login_page()
else:
    main_app()
