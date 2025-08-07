from langchain_groq import ChatGroq
# Removed import for GROQ_API_KEY from config.config for debugging purposes.
# We will directly use os.getenv() for the API key here.
from config.config import GROQ_MODEL_NAME # Keep this if you're using it for model names
import os

def load_llm(mode="Concise"):
    # Determine the model name based on the mode
    model = "llama3-8b-8192" if mode == "Concise" else "llama3-70b-8192"

    print(f"DEBUG LLM: Attempting to load ChatGroq with model: {model} for mode: {mode}")

    # Directly retrieve API key from environment variables
    api_key_to_use = os.getenv("GROQ_API_KEY")

    if not api_key_to_use:
        print("CRITICAL ERROR LLM: GROQ_API_KEY is NOT available from os.getenv(). Cannot initialize LLM.")
        raise ValueError("GROQ_API_KEY is not configured. Cannot initialize LLM.")

    print(f"DEBUG LLM: GROQ_API_KEY is loaded successfully (starts with: {api_key_to_use[:5]}...)")
    print(f"DEBUG LLM: Attempting ChatGroq initialization with model='{model}' and API key.")

    try:
        # This is the line where the error is most likely occurring
        llm_instance = ChatGroq(groq_api_key=api_key_to_use, model_name=model)
        print(f"DEBUG LLM: ChatGroq instance created successfully for model: {model}")
        return llm_instance
    except Exception as e:
        print(f"CRITICAL ERROR LLM: Failed to initialize ChatGroq for model {model}: {e}")
        # Re-raise the exception to propagate it up to app.py and show in Streamlit UI
        raise

