import streamlit as st

st.set_page_config(page_title="Fuel Station Login")

# Hardcoded credentials (can later move to DB)
USERNAME = "admin"
PASSWORD = "fuel123"

st.title("Admin Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.button("Login"):
    if username == USERNAME and password == PASSWORD:
        st.session_state.logged_in = True
        st.success("Login successful")
        st.switch_page("Details.py")
    else:
        st.error("Invalid username or password")
