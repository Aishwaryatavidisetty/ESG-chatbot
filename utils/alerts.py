import google.generativeai as genai
from config.config import GEMINI_API_KEY

def fetch_esg_alerts():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-pro-1.5")  # ✅ Correct model
        prompt = "List the latest 5 ESG regulations or news in 2025 with sources."
        response = model.generate_content(prompt)
        return [response.text]  # ✅ You can customize splitting if needed
    except Exception as e:
        return [f"Error fetching alerts from Gemini: {e}"]
