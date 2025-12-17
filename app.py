import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import smtplib
from email.message import EmailMessage

# ================= UI =================
st.title("⛽ Petrol Bunk Daily Report")
date = st.date_input("Date")

# ---------------- PETROL ----------------
st.header("🟢 PETROL DETAILS")
p_opening = st.number_input("Petrol Opening Stock (Litres)", 0.0)
p_added = st.number_input("Petrol Stock Added (Litres)", 0.0)
p_closing = st.number_input("Petrol Closing Stock (Litres)", 0.0)
p_price = st.number_input("Petrol Price per Litre (₹)", 0.0)

p_fuel_sold = p_opening + p_added - p_closing
p_expected = p_fuel_sold * p_price

# ---------------- DIESEL ----------------
st.header("🔵 DIESEL DETAILS")
d_opening = st.number_input("Diesel Opening Stock (Litres)", 0.0)
d_added = st.number_input("Diesel Stock Added (Litres)", 0.0)
d_closing = st.number_input("Diesel Closing Stock (Litres)", 0.0)
d_price = st.number_input("Diesel Price per Litre (₹)", 0.0)

d_fuel_sold = d_opening + d_added - d_closing
d_expected = d_fuel_sold * d_price

# ---------------- PAYMENTS ----------------
st.header("💰 PAYMENT COLLECTION")
cash = st.number_input("Total Cash Collected (₹)", 0.0)
digital = st.number_input("Total Digital Payment (₹)", 0.0)

total_collected = cash + digital
total_expected = p_expected + d_expected
difference = total_collected - total_expected

# ---------------- SUMMARY ----------------
st.subheader("📊 DAILY SUMMARY")
st.write("Petrol Sold:", p_fuel_sold, "L")
st.write("Diesel Sold:", d_fuel_sold, "L")
st.write("Total Expected: ₹", total_expected)
st.write("Total Collected: ₹", total_collected)

if difference < 0:
    st.error(f"❌ Shortage: ₹{abs(difference)}")
else:
    st.success(f"✅ Excess: ₹{difference}")

# ================= PDF =================
def generate_pdf(data):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)
    width, height = A4
    y = height - 60

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, "BRUNDAVANA FUEL STATION")
    y -= 30
    c.setFont("Helvetica", 13)
    c.drawCentredString(width/2, y, "Daily Sales Report")
    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(60, y, "PETROL")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(80, y, f"Sold: {data['petrol_sold']} L")
    y -= 18
    c.drawString(80, y, f"Revenue: ₹{data['petrol_revenue']}")
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(60, y, "DIESEL")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(80, y, f"Sold: {data['diesel_sold']} L")
    y -= 18
    c.drawString(80, y, f"Revenue: ₹{data['diesel_revenue']}")
    y -= 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, y, "TOTAL CASH COLLECTED")
    y -= 25
    c.setFont("Helvetica-Bold", 20)
    c.drawString(80, y, f"₹ {data['total_collected']}")
    y -= 35

    c.setFont("Helvetica-Bold", 14)
    if data["difference"] < 0:
        c.setFillColorRGB(1, 0, 0)
        c.drawString(60, y, f"SHORTAGE: ₹{abs(data['difference'])}")
    else:
        c.setFillColorRGB(0, 0.6, 0)
        c.drawString(60, y, f"EXCESS: ₹{data['difference']}")
    c.setFillColorRGB(0, 0, 0)

    c.save()
    return temp_file.name

# ================= EMAIL =================
def send_email(receiver_email, pdf_path, date):
    sender_email = "monishthimmaiah11@gmail.com"
    sender_password = "dobjcxwrufnvmeck"

    msg = EmailMessage()
    msg["Subject"] = f"Daily Petrol Bunk Report - {date}"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find attached the daily report.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="report.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

# ================= ACTIONS =================
pdf_data = {
    "petrol_sold": round(p_fuel_sold, 2),
    "petrol_revenue": round(p_expected, 2),
    "diesel_sold": round(d_fuel_sold, 2),
    "diesel_revenue": round(d_expected, 2),
    "total_collected": round(total_collected, 2),
    "difference": round(difference, 2)
}

st.subheader("📄 Download Report")
if st.button("Download PDF"):
    path = generate_pdf(pdf_data)
    with open(path, "rb") as f:
        st.download_button("Download", f, "daily_report.pdf")

st.subheader("📧 Send Report via Email")
receiver_email = st.text_input("Owner Email")
if st.button("Send Email"):
    path = generate_pdf(pdf_data)
    send_email(receiver_email, path, date)
    st.success("📨 Email sent successfully")
