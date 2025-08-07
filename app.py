import streamlit as st
import os
import sys
import fitz  # PyMuPDF
from langchain_core.messages import HumanMessage, AIMessage

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Local imports
from models.llm import load_llm
from models.embeddings import embed_documents
from utils.rag_utils import answer_with_rag
from utils.web_search import google_search
from utils.score_utils import calculate_esg_scores
from utils.alerts import fetch_esg_alerts

# --- Streamlit UI ---
st.set_page_config(page_title="ESG Reporting & Analysis Chatbot", layout="wide")
st.title("🌍 ESG Reporting & Analysis Chatbot")

# Sidebar controls
st.sidebar.header("💬 Chat History")
mode = st.sidebar.radio("Response Mode", ("Concise", "Detailed"))
clear_history = st.sidebar.button("🗑️ Clear Chat History")

if clear_history:
    st.session_state.messages = []

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tabs
tabs = st.tabs(["📤 Upload & Score", "💬 Chat Interface", "🔔 ESG Alerts"])

# --- Upload & Score ---
with tabs[0]:
    st.subheader("📤 Upload ESG Report")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        st.success("PDF extracted successfully.")
        # Embed and score
        embed_documents([text])
        esg_scores = calculate_esg_scores(text)
        st.write("### 🧮 ESG Scores")
        st.json(esg_scores)

# --- Chat Interface ---
with tabs[1]:
    st.subheader("💬 Ask ESG Questions")
    user_input = st.text_input("Enter your question:")
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Call RAG chain
        response = answer_with_rag(user_input, mode=mode)
        st.session_state.messages.append(AIMessage(content=response))

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").markdown(msg.content)
        else:
            st.chat_message("ai").markdown(msg.content)

# --- ESG Alerts ---
with tabs[2]:
    st.subheader("🔔 Live ESG Alerts")
    alerts = fetch_esg_alerts()
    for alert in alerts:
        st.markdown(alert)
