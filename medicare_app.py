import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("healthcare.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    district TEXT,
    disease TEXT,
    subtype TEXT,
    days_suffering INTEGER
)''')
conn.commit()

# Prescription database
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
    "throat pain": "Warm salt water gargle, lozenges, paracetamol if fever.",
    "period pain": "Mefenamic acid 250mg, hot water bag, rest and hydration.",
    "vomiting": "Ondansetron (as prescribed), drink ORS, avoid oily food.",
    "back pain": "Ibuprofen 400mg, gentle stretching, proper rest."
}

# Skin infection subtypes
skin_infection_prescriptions = {
    "fungal": "Apply antifungal cream (Clotrimazole), keep area dry, avoid tight clothes.",
    "bacterial": "Apply antibacterial ointment (Mupirocin), maintain hygiene.",
    "allergic": "Use antihistamine cream, avoid allergens, keep skin moisturized.",
    "eczema": "Moisturizing cream, mild steroid cream if prescribed, avoid scratching."
}

# Streamlit UI
st.title("Healthcare Prescription System")

with st.form("patient_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    district = st.text_input("District")
    disease = st.text_input("Disease")
    
    # Extra input for skin infection
    subtype = ""
    if disease.strip().lower() == "skin infection":
        subtype = st.selectbox("Type of Skin Infection", ["", "Fungal", "Bacterial", "Allergic", "Eczema"])
    
    days = st.number_input("Days Suffering", min_value=0, step=1)
    submitted = st.form_submit_button("Submit")

if submitted:
    if not (name and age and gender and district and disease and days):
        st.error("⚠️ All fields are required!")
    else:
        disease_key = disease.strip().lower()
        subtype_key = subtype.strip().lower() if subtype else None

        cur.execute("INSERT INTO patients (name, age, gender, district, disease, subtype, days_suffering) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, age, gender, district, disease_key, subtype_key, days))
        conn.commit()

        if days > 3:
            prescription = "⚠️ You have been suffering for more than 3 days. Please consult a doctor immediately."
        else:
            if disease_key == "skin infection":
                if subtype_key and subtype_key in skin_infection_prescriptions:
                    prescription = skin_infection_prescriptions[subtype_key]
                else:
                    prescription = "Please specify the type of skin infection for accurate prescription."
            else:
                prescription = prescriptions.get(disease_key, "No exact match found. Please consult a doctor.")

        st.success(f"✅ Prescription Generated for {name}")
        st.info(f"**Disease:** {disease.capitalize()} {('('+subtype.capitalize()+')') if subtype else ''}\n\n**Prescription:** {prescription}")

# Show patient records
st.subheader("📋 Patient Records")
cur.execute("SELECT * FROM patients")
rows = cur.fetchall()

if rows:
    df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Gender", "District", "Disease", "Subtype", "Days Suffering"])
    st.dataframe(df, use_container_width=True)
else:
    st.write("No patient records yet.")
