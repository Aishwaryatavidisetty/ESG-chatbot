import os

# If running on Streamlit Cloud, use st.secrets
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    GOOGLE_CX = st.secrets["GOOGLE_CX"]
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]

except Exception:
    # Local development fallback to .env
    from dotenv import load_dotenv
    load_dotenv()

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CX = os.getenv("GOOGLE_CX")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

