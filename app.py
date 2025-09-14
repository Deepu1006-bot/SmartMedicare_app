import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("healthcare.db", check_same_thread=False)
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
    "diabetes": "Metformin 500mg after meals, regular sugar check.",
    "hypertension": "Amlodipine 5mg daily, reduce salt intake, regular BP check.",
    "asthma": "Use inhaler as prescribed, avoid dust, do breathing exercises.",
    "malaria": "Chloroquine as per dosage, drink fluids, consult doctor if no improvement.",
    "typhoid": "Ciprofloxacin (as prescribed), take boiled water, light diet.",
    "allergy": "Antihistamine (Loratadine), avoid allergens, drink water.",
    "migraine": "Ibuprofen 400mg if needed, rest in dark room, avoid triggers.",
    "cholera": "ORS solution frequently, antibiotics if prescribed, hydration is key.",
    "covid": "Paracetamol for fever, isolation, steam inhalation, consult doctor if severe.",
    "tuberculosis": "Antitubercular drugs (as prescribed), regular checkups.",
    "stomachache": "Drotaverine (as prescribed), drink warm water, avoid spicy food.",
    "acidity": "Pantoprazole 40mg before food, avoid oily & spicy meals.",
    "loose motion": "ORS solution, probiotics, avoid outside food.",
    "constipation": "High fiber diet, drink plenty of water, mild laxative if needed.",
    "skin infection": "Apply antifungal/antibacterial cream, keep area clean and dry.",
    "throat pain": "Warm salt water gargle, lozenges, paracetamol if fever.",
    "period pain": "Mefenamic acid 250mg, hot water bag, rest and hydration.",
    "vomiting": "Ondansetron (as prescribed), drink ORS, avoid oily food.",
    "back pain": "Ibuprofen 400mg, gentle stretching, proper rest."
}

symptoms_map = {
    "high temperature": "fever",
    "chills": "malaria",
    "sneezing": "cold",
    "runny nose": "cold",
    "dry cough": "cough",
    "severe cough": "tuberculosis",
    "body pain": "fever",
    "thirst": "diabetes",
    "frequent urination": "diabetes",
    "head pain": "headache",
    "eye pain": "migraine",
    "chest tightness": "asthma",
    "shortness of breath": "asthma",
    "loose stools": "loose motion",
    "abdominal pain": "stomachache",
    "acidity": "acidity",
    "irregular periods": "period pain",
    "vomit": "vomiting",
    "skin rash": "skin infection",
    "itching": "skin infection",
    "backache": "back pain",
    "sore throat": "throat pain"
}

st.title("Healthcare Prescription System 🏥")

with st.form("patient_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    district = st.text_input("District")
    disease_or_symptom = st.text_input("Disease / Symptom")
    days = st.number_input("Days Suffering", min_value=0, step=1)
    submitted = st.form_submit_button("Submit")

if submitted:
    if not (name and age and gender and district and disease_or_symptom and days):
        st.error("⚠️ All fields are required!")
    else:
        input_key = disease_or_symptom.strip().lower()
        if input_key in symptoms_map:
            disease_key = symptoms_map[input_key]
        else:
            disease_key = input_key
        cur.execute("INSERT INTO patients (name, age, gender, district, disease, days_suffering) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, age, gender, district, disease_key, days))
        conn.commit()
        if days > 3:
            prescription = "⚠️ You have been suffering for more than 3 days. Please consult a doctor immediately."
        else:
            prescription = prescriptions.get(disease_key, "❌ No exact match found. Please consult a doctor.")
        st.success(f"✅ Prescription Generated for {name}")
        st.info(f"**Disease Identified:** {disease_key.capitalize()}\n\n**Prescription:** {prescription}")

st.subheader("📋 Patient Records")
cur.execute("SELECT * FROM patients")
rows = cur.fetchall()
if rows:
    df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Gender", "District", "Disease", "Days Suffering"])
    st.dataframe(df, use_container_width=True)
else:
    st.write("No patient records yet.")
