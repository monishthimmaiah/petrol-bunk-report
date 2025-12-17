import streamlit as st
from datetime import date

st.set_page_config(page_title="Enter Daily Details")

if not st.session_state.get("logged_in", False):
    st.error("Please login first")
    st.stop()

st.title("Daily Fuel Entry")
st.subheader("Welcome, Brundavana Fuel Station")

report_date = st.date_input("Date", date.today())

# -------- PETROL --------
st.header("🟢 Petrol")
p_open = st.number_input("Opening Stock (L)", 0.0)
p_added = st.number_input("Stock Added (L)", 0.0)
p_close = st.number_input("Closing Stock (L)", 0.0)
p_price = st.number_input("Price/Litre (₹)", 0.0)

# -------- DIESEL --------
st.header("🔵 Diesel")
d_open = st.number_input("Diesel Opening (L)", 0.0)
d_added = st.number_input("Diesel Added (L)", 0.0)
d_close = st.number_input("Diesel Closing (L)", 0.0)
d_price = st.number_input("Diesel Price/Litre (₹)", 0.0)

# -------- PAYMENTS --------
st.header("💰 Payments")
cash = st.number_input("Cash Collected (₹)", 0.0)
digital = st.number_input("Digital Payments (₹)", 0.0)

if st.button("Submit & View Summary"):
    st.session_state.data = {
        "date": report_date,

        "p_open": p_open,
        "p_added": p_added,
        "p_close": p_close,
        "p_price": p_price,

        "d_open": d_open,
        "d_added": d_added,
        "d_close": d_close,
        "d_price": d_price,

        "cash": cash,
        "digital": digital
    }
    st.switch_page("pages/Summary.py")
    
