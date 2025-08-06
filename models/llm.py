from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

def load_llm(temperature=0.2):
    return ChatGroq(model="llama3-8b-8192", temperature=temperature, groq_api_key=GROQ_API_KEY)
