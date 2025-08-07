from langchain_groq import ChatGroq
# Assuming config.py is correctly set up to load these from environment variables
from config.config import GROQ_API_KEY, GROQ_MODEL_NAME
import os # Fallback for getting env vars if config.py isn't working as expected

def load_llm(mode="Concise"):
    # Use GROQ_MODEL_NAME from config.py if it's set, otherwise default
    default_model = GROQ_MODEL_NAME if GROQ_MODEL_NAME else "llama3-8b-8192"
    model = "llama3-8b-8192" if mode == "Concise" else "llama3-70b-8192"

    print(f"DEBUG LLM: Attempting to load ChatGroq with model: {model} for mode: {mode}")

    # Ensure GROQ_API_KEY is available. Check config.py first, then os.getenv as fallback.
    api_key_to_use = GROQ_API_KEY
    if not api_key_to_use:
        api_key_to_use = os.getenv("GROQ_API_KEY")
        print("DEBUG LLM: GROQ_API_KEY not found via config.py, attempting os.getenv.")

    if not api_key_to_use:
        print("ERROR LLM: GROQ_API_KEY is not available in load_llm function.")
        raise ValueError("GROQ_API_KEY is not configured. Cannot initialize LLM.")

    print(f"DEBUG LLM: GROQ_API_KEY is loaded (starts with: {api_key_to_use[:5]}...)")

    try:
        llm_instance = ChatGroq(groq_api_key=api_key_to_use, model_name=model)
        print(f"DEBUG LLM: ChatGroq instance created successfully for model: {model}")
        return llm_instance
    except Exception as e:
        print(f"ERROR LLM: Failed to initialize ChatGroq for model {model}: {e}")
        # Re-raise the exception to propagate it up to app.py and show in Streamlit UI
        raise

