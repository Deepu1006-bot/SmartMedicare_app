import streamlit as st
import sqlite3

conn = sqlite3.connect("healthcare.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    district TEXT,
    disease TEXT,
    days_suffering INTEGER
)''')
conn.commit()

prescriptions = {
    "fever": "Paracetamol 500mg twice a day, stay hydrated, take rest.",
    "cold": "Cetrizine 10mg once daily, steam inhalation, warm fluids.",
    "cough": "Cough syrup (dextromethorphan), honey with warm water.",
    "headache": "Paracetamol 500mg if needed, good sleep, avoid stress.",
    "diabetes": "Metformin 500mg after meals, regular sugar check."
}

st.title("💊 Healthcare Prescription System")

with st.form("patient_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    district = st.text_input("District")
    disease = st.text_input("Disease").lower()
    days = st.number_input("Days Suffering", min_value=0, step=1)
    submitted = st.form_submit_button("Submit")

if submitted:
    if not (name and age and gender and district and disease and days):
        st.error("⚠️ All fields are required!")
    else:
        cur.execute("INSERT INTO patients (name, age, gender, district, disease, days_suffering) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, age, gender, district, disease, days))
        conn.commit()
        prescription = prescriptions.get(disease, "Consult a doctor for detailed prescription.")
        st.success(f"✅ Prescription Generated for {name}")
        st.info(f"**Disease:** {disease.capitalize()}\n\n**Prescription:** {prescription}")
