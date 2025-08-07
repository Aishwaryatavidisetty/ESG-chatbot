import os

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")