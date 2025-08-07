from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL_NAME

def load_llm(mode="Concise"):
    model = "llama3-8b-8192" if mode == "Concise" else "llama3-70b-8192"
    return ChatGroq(groq_api_key=GROQ_API_KEY, model_name=model)