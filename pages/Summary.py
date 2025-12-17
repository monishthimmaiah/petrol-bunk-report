import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import tempfile, os, smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Summary & Report")

# ---------- Session Check ----------
if "data" not in st.session_state:
    st.error("No data found. Please enter details first.")
    st.stop()

d = st.session_state.data

# ---------- Calculations ----------
p_sold = d["p_open"] + d["p_added"] - d["p_close"]
d_sold = d["d_open"] + d["d_added"] - d["d_close"]

p_revenue = p_sold * d["p_price"]
d_revenue = d_sold * d["d_price"]

expected = p_revenue + d_revenue
collected = d["cash"] + d["digital"]
difference = collected - expected

# ---------- Stock Left ----------
petrol_closing_stock = d["p_close"]
diesel_closing_stock = d["d_close"]

petrol_price = d["p_price"]
diesel_price = d["d_price"]

petrol_stock_value = petrol_closing_stock * petrol_price
diesel_stock_value = diesel_closing_stock * diesel_price
total_stock_value = petrol_stock_value + diesel_stock_value

# ---------- UI ----------
st.title("📊 Daily Summary")

st.metric("Petrol Sold (L)", round(p_sold, 2))
st.metric("Diesel Sold (L)", round(d_sold, 2))
st.metric("Total Expected (₹)", round(expected, 2))
st.metric("Total Collected (₹)", round(collected, 2))
st.metric("Fuel Stock Value (₹)", round(total_stock_value, 2))

if difference < 0:
    st.error(f"❌ Shortage: ₹{abs(round(difference,2))}")
else:
    st.success(f"✅ Excess: ₹{round(difference,2)}")

# ---------- PDF FUNCTION ----------
def generate_pdf():
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name, pagesize=A4)
    w, h = A4
    y = h - 50

    # ---------- LOGO ----------
    if os.path.exists("logo.png"):
        c.drawImage("logo.png", 40, h - 90, 120, 50, preserveAspectRatio=True)

    # ---------- HEADER ----------
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, y, "BRUNDAVANA FUEL STATION")
    y -= 28

    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, y, "Daily Sales & Stock Report")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Date: {d['date']}")
    y -= 20

    c.line(40, y, w - 40, y)
    y -= 30

    # ================= PETROL =================
    c.setFillColorRGB(0.85, 0.95, 0.85)
    c.rect(40, y - 90, w - 80, 90, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 20, "PETROL")

    c.setFont("Helvetica", 11)
    c.drawString(50, y - 40, f"Sold: {round(p_sold,2)} L")
    c.drawRightString(w - 50, y - 40, f"Revenue: ₹ {round(p_revenue,2)}")

    c.drawString(50, y - 60, f"Stock Left: {round(petrol_closing_stock,2)} L")
    c.drawRightString(w - 50, y - 60, f"Stock Value: ₹ {round(petrol_stock_value,2)}")

    y -= 110

    # ================= DIESEL =================
    c.setFillColorRGB(0.85, 0.90, 0.97)
    c.rect(40, y - 90, w - 80, 90, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 20, "DIESEL")

    c.setFont("Helvetica", 11)
    c.drawString(50, y - 40, f"Sold: {round(d_sold,2)} L")
    c.drawRightString(w - 50, y - 40, f"Revenue: ₹ {round(d_revenue,2)}")

    c.drawString(50, y - 60, f"Stock Left: {round(diesel_closing_stock,2)} L")
    c.drawRightString(w - 50, y - 60, f"Stock Value: ₹ {round(diesel_stock_value,2)}")

    y -= 120

    # ================= TOTAL =================
    c.setFont("Helvetica-Bold", 15)
    c.drawString(40, y, "TOTAL SUMMARY")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawString(60, y, f"Expected Revenue : ₹ {round(expected,2)}")
    y -= 16
    c.drawString(60, y, f"Cash Collected   : ₹ {round(d['cash'],2)}")
    y -= 16
    c.drawString(60, y, f"Digital Payments : ₹ {round(d['digital'],2)}")
    y -= 16

    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, y, f"Total Collected  : ₹ {round(collected,2)}")
    y -= 25

    # ================= VARIANCE =================
    c.setFont("Helvetica-Bold", 14)

    if difference < 0:
        c.setFillColorRGB(1, 0, 0)
        c.drawString(40, y, f"SHORTAGE : ₹ {abs(round(difference,2))}")
    else:
        c.setFillColorRGB(0, 0.6, 0)
        c.drawString(40, y, f"EXCESS : ₹ {round(difference,2)}")

    c.setFillColorRGB(0, 0, 0)
    y -= 30

    # ================= FOOTER =================
    c.line(40, 90, w - 40, 90)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(40, 70, f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    c.save()
    return temp.name

# ---------- EMAIL FUNCTION ----------
def send_email(receiver_email, pdf_path):
    sender_email = "monishthimmaiah11@gmail.com"
    sender_password = "vifsawmkdjeqhiih"

    msg = EmailMessage()
    msg["Subject"] = f"Daily Petrol Bunk Report - {d['date']}"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Please find attached the daily petrol bunk report.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="daily_report.pdf"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

# ---------- ACTIONS ----------
st.subheader("📄 Report Actions")

if st.button("Download PDF"):
    path = generate_pdf()
    with open(path, "rb") as f:
        st.download_button("Download Report", f, "daily_report.pdf")

st.subheader("📧 Email Report")
email = st.text_input("Owner Email")

if st.button("Send PDF via Email"):
    if not email:
        st.warning("Please enter an email address")
    else:
        path = generate_pdf()
        send_email(email, path)
        st.success("📧 Email sent successfully")
