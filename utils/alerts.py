import google.generativeai as genai
import os

def fetch_esg_alerts():
    try:
        # Load Gemini API Key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # Instantiate Gemini model
        model = genai.GenerativeModel("gemini-pro")

        # Define the query
        query = "List the top 5 latest ESG regulations or updates in 2025 with links if available."

        # Get the response
        response = model.generate_content(query)

        # Extract text
        content = response.text.strip()

        # Split into list based on line breaks or numbering
        lines = content.split("\n")
        alerts = [line for line in lines if line.strip()]

        return alerts[:5] if alerts else ["No alerts found."]
    
    except Exception as e:
        return [f"Error fetching alerts from Gemini: {e}"]
