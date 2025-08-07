# config/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load .env file if running locally

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama3-8b-8192") # Default model