import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class AgricultureAgent:
    """
    AI Agent using:
    1) ML model for crop prediction
    2) Groq LLaMA-3 for expert advisory
    """

    def __init__(self, model):
        self.model = model

        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        self.client = Groq(api_key=self.api_key)

    # -----------------------------
    # BASIC ML CROP RECOMMENDATION
    # -----------------------------
    def get_basic_crop(self, input_df):
        prediction = self.model.predict(input_df)
        return int(prediction[0])

    # -----------------------------
    # CLINIC-LEVEL AI ADVISORY
    # -----------------------------
    def get_exact_crop_guide(
        self,
        crop_name,
        location,
        soil_type,
        soil_ph,
        N, P, K,
        temperature,
        humidity,
        rainfall
    ):
        prompt = f"""
You are an experienced agricultural scientist.

Crop: {crop_name}
Location: {location}

Soil:
- Type: {soil_type}
- pH: {soil_ph}
- NPK: {N}, {P}, {K}

Weather:
- Temperature: {temperature} °C
- Humidity: {humidity} %
- Rainfall: {rainfall} mm

Give a step-by-step crop advisory:
1. Land preparation
2. Sowing & spacing
3. Fertilizer schedule
4. Irrigation plan
5. Disease & pest prevention
6. Harvesting tips

Write in simple farmer-friendly English.
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an agricultural expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )

        return response.choices[0].message.content
