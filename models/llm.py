from langchain_google_genai import ChatGoogleGenerativeAI
from config.config import GEMINI_API_KEY

def load_llm():
    return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
