import os
import google.generativeai as genai

# Load Gemini API key from env or st.secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def google_search(query):
    try:
        model = genai.GenerativeModel("gemini-pro")

        # Ask Gemini for web-style search results
        prompt = f"Give me a list of the top 3 latest web results (with titles and links if available) for: {query}"

        response = model.generate_content(prompt)
        content = response.text.strip()

        results = content.split("\n")
        return "\n".join(results[:6]) if results else "No results found."
    
    except Exception as e:
        return f"Error using Gemini for web search: {e}"
