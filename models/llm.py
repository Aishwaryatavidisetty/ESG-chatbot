from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL_NAME

def load_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL_NAME
    )
