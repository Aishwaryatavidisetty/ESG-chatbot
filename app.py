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

st.set_page_config(page_title="🌱 ESG AI Chatbot", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "documents" not in st.session_state:
    st.session_state.documents = []
if "response_mode" not in st.session_state:
    st.session_state.response_mode = "Detailed"

st.title("🌍 ESG Reporting & Analysis Chatbot")
tabs = st.tabs(["📤 Upload & Score", "💬 Chat Interface", "🔔 ESG Alerts"])

with tabs[0]:
    uploaded_files = st.file_uploader("Upload ESG Reports (PDFs)", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.documents = []
        for i, uploaded_file in enumerate(uploaded_files):
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                text = " ".join([page.get_text() for page in doc])
                embed_documents([text], index_path=f'vector_store/faiss_index_{i}')
                st.session_state.documents.append((f"Report {i+1}", text))
        st.success("✅ All documents embedded!")

        st.subheader("📊 ESG Score Comparisons")
        for name, doc_text in st.session_state.documents:
            scores = calculate_esg_scores(doc_text)
            st.markdown(f"#### {name}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Environmental", f"{scores['Environmental']}%")
            col2.metric("Social", f"{scores['Social']}%")
            col3.metric("Governance", f"{scores['Governance']}%")

with tabs[1]:
    st.sidebar.title("💬 Chat History")
    st.session_state.response_mode = st.sidebar.radio("Response Mode", ["Concise", "Detailed"], index=1)

    if st.sidebar.button("🗑 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask a question about ESG reports or policies")
    if query:
        try:
            with st.spinner("Thinking..."):
                answer = answer_with_rag(query)
                if not answer or "I don't know" in answer.lower():
                    st.warning("Answer not found in document. Searching the web...")
                    answer = google_search(query)

                if st.session_state.response_mode == "Concise":
                    answer = "- " + "\n- ".join(answer.split("\n")[:3])

                st.session_state.messages.append({"role": "user", "content": query})
                st.session_state.messages.append({"role": "assistant", "content": answer})

                with st.chat_message("user"):
                    st.markdown(query)
                with st.chat_message("assistant"):
                    st.markdown(answer)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

with tabs[2]:
    st.header("🔔 Live ESG Alerts")
    alerts = fetch_esg_alerts()
    for alert in alerts:
        st.markdown(alert)
        st.markdown("---")
