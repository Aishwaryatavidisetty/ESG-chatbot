import google.generativeai as genai
from config.config import GEMINI_API_KEY

def load_llm():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro-1.5')
    return model
