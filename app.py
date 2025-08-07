
import streamlit as st
import os
import sys
import fitz
from langchain_core.messages import HumanMessage, AIMessage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.llm import load_llm
from utils.rag_utils import answer_with_rag
from utils.web_search import google_search
from utils.score_utils import calculate_esg_scores
from models.embeddings import embed_documents
from utils.alerts import fetch_esg_alerts

st.set_page_config(page_title="ESG Chatbot", layout="wide")
st.title("🌍 ESG Reporting & Analysis Chatbot")

tabs = st.tabs(["📥 Upload & Score", "💬 Chat Interface", "🔔 ESG Alerts"])

# Upload & Score
with tabs[0]:
    uploaded_file = st.file_uploader("Upload ESG Report (PDF)", type=["pdf"])
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        st.subheader("Raw Text Extract")
        st.text_area("Extracted Text", text, height=200)

        if st.button("Embed & Score"):
            for i in range(0, len(text), 3000):
                chunk = text[i:i + 3000]
                embed_documents([chunk], index_path=f'vector_store/faiss_index_{i}')

            st.success("Embedding completed!")
            scores = calculate_esg_scores(text)
            st.subheader("ESG Scores")
            st.json(scores)

# Chat Interface
with tabs[1]:
    st.subheader("Chat with your ESG Data")
    user_input = st.text_input("Ask a question:")
    if user_input:
        response = answer_with_rag(user_input)
        st.write(response)

# ESG Alerts
with tabs[2]:
    st.subheader("🔔 Live ESG Alerts")
    alerts = fetch_esg_alerts()
    for alert in alerts:
        st.markdown(alert)
