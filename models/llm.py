from langchain_groq import ChatGroq
import streamlit as st

def load_llm():
    return ChatGroq(
        api_key=st.secrets["GROQ_API_KEY"],
        model="mixtral-8x7b-32768"  # or llama3-8b, llama3-70b
    )
