import streamlit as st
import os
import fitz
from models.llm import load_llm
from utils.rag_utils import answer_with_rag
from utils.score_utils import calculate_esg_scores
from models.embeddings import embed_documents
from utils.alerts import fetch_esg_alerts

st.set_page_config(page_title="ESG Reporting & Analysis Chatbot")
st.title("🌍 ESG Reporting & Analysis Chatbot")

# Sidebar
st.sidebar.header("💬 Chat History")
mode = st.sidebar.radio("Response Mode", ["Concise", "Detailed"])
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.clear()

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Score", "💬 Chat Interface", "🔔 ESG Alerts"])

# Upload Tab
with tab1:
    st.header("Upload ESG Report")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file:
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        st.success("PDF extracted successfully.")
        st.write(text[:1000] + "...")

        if st.button("🔍 Score ESG Report"):
            embed_documents([text])
            e_score, s_score, g_score = calculate_esg_scores(text)
            st.subheader("ESG Scores")
            st.write(f"🌱 Environment: {e_score}")
            st.write(f"🤝 Social: {s_score}")
            st.write(f"🏛️ Governance: {g_score}")

# Chat Tab
with tab2:
    st.header("Ask ESG Questions")
    user_input = st.text_input("Enter your question:")
    if user_input:
        try:
            response = answer_with_rag(user_input, mode=mode)
            st.success(response)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Alerts Tab
with tab3:
    st.header("🔔 Live ESG Alerts")
    alerts = fetch_esg_alerts()
    for alert in alerts:
        st.write(alert)

