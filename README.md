# 🌾 Smart Agriculture Advisory Agent

Smart Agriculture Advisory Agent is an AI-based application that recommends suitable crops and provides expert-level farming guidance using Machine Learning and AI Agents.

---

## 📌 Project Description

Farmers often face difficulties in selecting the right crop based on soil, weather, and location conditions.  
This project solves the problem by combining:
- Machine Learning for crop recommendation
- AI Agent (LLM via Groq – LLaMA 3.1) for detailed farming advisory

---

## 🎯 Objectives

- Recommend the best crop based on soil and weather data
- Provide step-by-step farming guidance
- Help farmers with fertilizer, irrigation, and disease prevention
- Build a real-world AI Agent–based system

---

## 🧠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Groq API (LLaMA 3.1)
- Pandas, NumPy
- Git & GitHub

---

## 📊 Input Parameters

- District
- Season
- Soil Type
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Soil pH
- Temperature
- Humidity
- Rainfall

---
## 🧪 Dataset Information

- Agriculture dataset with more than 10,000 records
- Contains soil, climate, rainfall, season, and crop data
- Data inspired by government and agricultural research sources

---

## 🚀 How the System Works

1. User enters soil, weather, and location details
2. Machine Learning model predicts the suitable crop
3. AI Agent generates detailed farming advisory
4. Results are displayed through a user-friendly web interface

---
### 📂 Project Structure

Smart-Agriculture-Advisory-Agent/
│
├── app.py
├── crop_recommendation_model.pkl
├── README.md
├── .env
└── .gitignore


## 📤 Output

- Recommended Crop
- Explainable AI (Why this crop?)
- AI-generated expert crop guide:
  - Land preparation
  - Sowing method
  - Fertilizer schedule
  - Irrigation plan
  - Disease prevention
  - Harvesting tips

---

## 🚀 How to Run the Project

## Step 1: Clone Repository
```bash
git clone https://github.com/USERNAME/Smart-Agriculture-Advisory-Agent.git
cd Smart-Agriculture-Advi sory-Agent

### Step 2: Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate
Step 3: Install Requirements
pip install streamlit pandas scikit-learn joblib groq python-dotenv

## Step 4: Setup .env

Create .env file:

GROQ_API_KEY=your_api_key_here

## Step 5: Run App
streamlit run app.py

-------


#### 🔮 Future Enhancements

- Multi-language support (Marathi / Hindi)
- Crop disease detection using images
- Real-time weather API integration
- Yield prediction
- SMS and WhatsApp alerts for farmers

---

## 👤 Author

**Aniket Dombale**  
Data Science & AI Enthusiast  

-------

⭐ If you find this project useful, feel free to star the repository.



