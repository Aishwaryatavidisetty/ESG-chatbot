import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_MODEL_NAME = "llama3-70b-8192"  # ✅ Valid Groq model
