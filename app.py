import streamlit as st
import pandas as pd
import joblib
from agent import AgricultureAgent

# ===============================
# APP CONFIG
# ===============================
st.set_page_config(page_title="Smart Agriculture Advisory Agent", layout="centered")
st.title("🌾 Smart Agriculture Advisory Agent")

# ===============================
# LOAD MODEL & AGENT
# ===============================
model = joblib.load("crop_recommendation_model.pkl")
agent = AgricultureAgent(model)

# ===============================
# LOCATION DATA
# ===============================
location_data = {
    "India": {
        "Maharashtra": {
            "Pune": ["Haveli", "Mulshi"],
            "Solapur": ["Pandharpur", "Barshi"],
            "Nashik": ["Igatpuri", "Sinnar"]
        },
        "Karnataka": {
            "Bangalore": ["North", "South"]
        },
        "Gujarat": {},
        "Uttar Pradesh": {}
    }
}

# ===============================
# LOCATION UI
# ===============================
st.subheader("📍 Location Selection")

country = st.selectbox("Country", list(location_data.keys()))
state = st.selectbox("State", list(location_data[country].keys()))

districts = list(location_data[country][state].keys())
district = None
city = None

if districts:
    district = st.selectbox("District", districts)
    city = st.selectbox("City / Taluka", location_data[country][state][district])
    st.success(f"Selected Location: {city}, {district}, {state}, {country}")
else:
    st.warning("District data will be added soon for this state.")

# ===============================
# SOIL DETAILS
# ===============================
st.subheader("🌱 Soil Details")

soil_type = st.selectbox("Soil Type", ["Black", "Loamy", "Sandy"])
N = st.number_input("Nitrogen (N)", 0, 150, 75)
P = st.number_input("Phosphorus (P)", 0, 150, 40)
K = st.number_input("Potassium (K)", 0, 150, 55)
soil_ph = st.number_input("Soil pH", 4.0, 9.0, 7.0)

# ===============================
# WEATHER DETAILS
# ===============================
st.subheader("🌦️ Weather Details")

season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid"])
temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.number_input("Humidity (%)", 0.0, 100.0, 60.0)
rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 110.0)

# ===============================
# ENCODING
# ===============================
district_map = {"Pune": 1, "Solapur": 2, "Nashik": 3}
season_map = {"Kharif": 0, "Rabi": 1, "Zaid": 2}
soil_map = {"Black": 0, "Loamy": 1, "Sandy": 2}

district_enc = district_map.get(district, 0)
season_enc = season_map.get(season, 0)
soil_enc = soil_map.get(soil_type, 0)

# ===============================
# CROP KNOWLEDGE BASE
# ===============================
crop_info = {
    "Rice": {
        "Climate": "Warm and humid climate with good rainfall",
        "Sowing": "June – July",
        "Seed_Rate": "20–25 kg/ha",
        "Irrigation": "Standing water required",
        "Fertilizer": "High nitrogen with split NPK",
        "Diseases": "Leaf Blast, Brown Spot",
        "Harvest": "120–150 days",
        "Expected_Yield": "25–30 quintals/acre"
    },
    "Wheat": {
        "Climate": "Cool and dry",
        "Sowing": "Oct – Nov",
        "Seed_Rate": "100–125 kg/ha",
        "Irrigation": "4–5 irrigations",
        "Fertilizer": "Balanced NPK",
        "Diseases": "Rust, Smut",
        "Harvest": "110–130 days",
        "Expected_Yield": "20–25 quintals/acre"
    },
    "Onion": {
        "Climate": "Mild temperature",
        "Sowing": "Oct–Nov / Jun–Jul",
        "Seed_Rate": "8–10 kg/ha",
        "Irrigation": "Light but frequent",
        "Fertilizer": "High potassium",
        "Diseases": "Purple Blotch, Thrips",
        "Harvest": "90–120 days",
        "Expected_Yield": "150–250 quintals/acre"
    },
    "Vegetables": {
        "Climate": "Crop specific",
        "Sowing": "Year round",
        "Seed_Rate": "Varies",
        "Irrigation": "Frequent light irrigation",
        "Fertilizer": "Organic + NPK",
        "Diseases": "Leaf Curl, Blight",
        "Harvest": "30–90 days",
        "Expected_Yield": "Varies"
    }
}

# ===============================
# AI AGENT BUTTON
# ===============================
st.markdown("---")
st.subheader("🤖 AI Agent Advisory")

exact_btn = st.button("🌐 Get Exact Clinic-Level Crop Guide (AI Agent)")

# ===============================
# AI AGENT LOGIC
# ===============================
if exact_btn and district and city:

    input_df = pd.DataFrame([[ 
        district_enc,
        season_enc,
        soil_enc,
        N, P, K,
        soil_ph,
        temperature,
        humidity,
        rainfall
    ]], columns=[
        "District", "Season", "Soil_Type",
        "N", "P", "K", "Soil_pH",
        "Temperature", "Humidity", "Rainfall"
    ])

    label = agent.get_basic_crop(input_df)

    crop_map = {
        0: "Rice",
        1: "Wheat",
        2: "Jowar",
        3: "Bajra",
        4: "Gram",
        5: "Onion",
        6: "Vegetables"
    }

    crop_name = crop_map.get(label, "Unknown")

    if crop_name == "Unknown":
        st.error("Crop not supported by current model.")
        st.stop()

    st.success(f"🌾 Crop Identified by AI Agent: **{crop_name}**")

    with st.spinner("AI Agent is generating expert advisory..."):
        guide = agent.get_exact_crop_guide(
            crop_name=crop_name,
            location=f"{city}, {district}, {state}, {country}",
            soil_type=soil_type,
            soil_ph=soil_ph,
            N=N, P=P, K=K,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall
        )

    st.subheader("🌐 Clinic-Level AI Crop Guide")
    st.write(guide)

    # Explainability
    st.subheader("🤖 Why this crop?")
    if rainfall > 100:
        st.write("✔️ Adequate rainfall")
    if 6.0 <= soil_ph <= 7.5:
        st.write("✔️ Suitable soil pH")
    if humidity < 70:
        st.write("✔️ Favorable humidity")
    st.write(f"✔️ Suitable for {season} season")

    # Crop Info
    if crop_name in crop_info:
        info = crop_info[crop_name]
        st.subheader("📘 Crop Summary")
        for k, v in info.items():
            st.write(f"**{k}:** {v}")
