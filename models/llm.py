from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

def load_llm(mode="Concise"):
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="mixtral-8x7b-32768",  # or llama3-70b
        temperature=0.7 if mode == "Concise" else 0.3
    )
