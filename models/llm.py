from langchain_groq import ChatGroq
from config import GROQ_API_KEY

def load_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192"
    )

