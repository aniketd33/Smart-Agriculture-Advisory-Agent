import streamlit as st
import pandas as pd
import joblib
from agent import AgricultureAgent

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart Agriculture Advisory Agent",
    layout="centered"
)

st.title("🌾 Smart Agriculture Advisory Agent")

# ===============================
# LOAD MODEL & AGENT
# ===============================
model = joblib.load("final_crop_recommendation_model.pkl")

le_district = joblib.load("le_district.pkl")
le_season = joblib.load("le_season.pkl")
le_soil = joblib.load("le_soil.pkl")
le_crop = joblib.load("le_crop.pkl")

agent = AgricultureAgent(model)

# ===============================
# USER INPUT
# ===============================
st.subheader("📍 Location & Soil Details")

district = st.selectbox("District", le_district.classes_)
season = st.selectbox("Season", le_season.classes_)
soil_type = st.selectbox("Soil Type", le_soil.classes_)

N = st.number_input("Nitrogen (N)", 0, 150, 50)
P = st.number_input("Phosphorus (P)", 0, 150, 40)
K = st.number_input("Potassium (K)", 0, 150, 40)

soil_ph = st.slider("Soil pH", 4.0, 9.0, 7.0)

st.subheader("🌦️ Weather Details")

temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.number_input("Humidity (%)", 0.0, 100.0, 60.0)
rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 100.0)

# ===============================
# CROP RECOMMENDATION
# ===============================
if st.button("🌾 Recommend Crop"):

    d_enc = le_district.transform([district])[0]
    s_enc = le_season.transform([season])[0]
    soil_enc = le_soil.transform([soil_type])[0]

    input_df = pd.DataFrame([[
        d_enc, s_enc, soil_enc,
        N, P, K,
        soil_ph, temperature, humidity, rainfall
    ]], columns=[
        "District", "Season", "Soil_Type",
        "N", "P", "K",
        "Soil_pH", "Temperature", "Humidity", "Rainfall"
    ])

    pred = model.predict(input_df)
    crop = le_crop.inverse_transform(pred)[0]

    st.success(f"✅ Recommended Crop: **{crop}**")

    # SAVE crop for next steps
    st.session_state["crop"] = crop
    st.session_state["input_df"] = input_df

# ===============================
# AI AGENT ADVISORY
# ===============================
st.markdown("---")
st.subheader("🤖 AI Agent Advisory")

if st.button("🌐 Get Expert Crop Guide (AI Agent)"):

    if "crop" not in st.session_state:
        st.error("❌ Please click 'Recommend Crop' first.")
        st.stop()

    crop = st.session_state["crop"]

    with st.spinner("AI Agent is generating expert crop guidance..."):
        guide = agent.get_exact_crop_guide(
            crop_name=crop,
            location=district,
            soil_type=soil_type,
            soil_ph=soil_ph,
            N=N, P=P, K=K,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall
        )

    st.subheader("🌱 Clinic-Level Crop Guidance")
    st.write(guide)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("Smart Agriculture Advisory Agent • ML + AI Powered 🌱")
