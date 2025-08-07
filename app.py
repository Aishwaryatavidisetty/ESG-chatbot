import streamlit as st
import os
import time
from dotenv import load_dotenv # To load environment variables locally

# --- Custom Module Imports ---
try:
    from models.llm import load_llm
    from utils.rag_utils import answer_with_rag
    from utils.alerts import fetch_esg_alerts
except ImportError as e:
    st.error(f"Error importing custom modules: {e}. Please ensure your file structure and module names are correct.")
    st.stop()

# --- Langchain and PDF Processing Imports ---
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from cohere.core.api_error import ApiError as CohereApiError

# Load environment variables (important for local testing, Streamlit Cloud handles secrets)
load_dotenv()

# --- API Keys ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# --- Critical API Key Validation ---
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is not set. Please configure it in your environment variables or Streamlit secrets.")
    st.stop()

if not COHERE_API_KEY:
    st.error("COHERE_API_KEY is not set. This key is required for PDF processing (embeddings). Please configure it in your environment variables or Streamlit secrets.")
    st.stop()

print(f"GROQ_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}, starts with: {GROQ_API_KEY[:5] if GROQ_API_KEY else 'N/A'}")
print(f"COHERE_API_KEY loaded: {'Yes' if COHERE_API_KEY else 'No'}, starts with: {COHERE_API_KEY[:5] if COHERE_API_KEY else 'N/A'}")


# --- Constants ---
FAISS_INDEX_PATH = 'vector_store/faiss_index'

# --- Helper Functions ---

def process_pdf_for_rag(uploaded_file):
    """
    Processes an uploaded PDF, chunks it, creates embeddings, and saves a FAISS index.
    """
    if uploaded_file is not None:
        st.info(f"Processing '{uploaded_file.name}' for RAG. This might take a moment...")
        try:
            temp_file_path = f"./temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(documents)

            st.info("Initializing Cohere Embeddings...")
            try:
                embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, model="embed-english-light-v3.0")
            except CohereApiError as e:
                st.error(f"Cohere API Error during embeddings initialization: {e}. This often means your COHERE_API_KEY is invalid or has insufficient permissions.")
                print(f"Cohere API Error details: {e}")
                os.remove(temp_file_path)
                return False
            except Exception as e:
                st.error(f"Unexpected error initializing Cohere Embeddings: {e}. Please check your internet connection or Cohere API key.")
                print(f"Unexpected Embeddings Error details: {e}")
                os.remove(temp_file_path)
                return False

            st.info("Creating FAISS index...")
            db = FAISS.from_documents(texts, embeddings)
            os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
            db.save_local(FAISS_INDEX_PATH)

            st.success(f"'{uploaded_file.name}' processed and FAISS index created successfully! You can now ask questions.")
            st.warning("Note: In Streamlit Cloud, this index is stored on an ephemeral filesystem and will be lost if the app restarts. For persistent storage, consider using cloud storage (e.g., Google Cloud Storage) or a dedicated vector database.")

            os.remove(temp_file_path)

            return True
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            print(f"Full PDF processing error: {e}")
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return False
    return False

# --- Streamlit UI Setup ---

st.set_page_config(page_title="ESG Reporting & Analysis Chatbot", layout="centered")

st.title("🌍 ESG Reporting & Analysis Chatbot")

# Initialize session state variables
if 'pdf_processed' not in st.session_state:
    st.session_state['pdf_processed'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'faiss_index_ready' not in st.session_state:
    st.session_state['faiss_index_ready'] = False
# Initialize a key for the chat_input widget to allow clearing it
if 'chat_input_key' not in st.session_state:
    st.session_state['chat_input_key'] = 0


if os.path.exists(FAISS_INDEX_PATH) and not st.session_state['faiss_index_ready']:
    st.session_state['faiss_index_ready'] = True
    st.session_state['pdf_processed'] = True
    st.info("FAISS index found from a previous session. Ready to chat!")


# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Upload & Score", "Chat Interface", "ESG Alerts"])

with tab1:
    st.header("Upload & Score ESG Documents")
    st.write("Upload your ESG PDF document here to enable the chatbot to answer questions based on its content.")
    uploaded_file = st.file_uploader("Upload your ESG PDF document", type="pdf", key="pdf_uploader")

    if uploaded_file:
        if not st.session_state['pdf_processed'] or st.button("Re-process this PDF", key="reprocess_button"):
            st.session_state['pdf_processed'] = False
            st.session_state['faiss_index_ready'] = False
            st.session_state['chat_history'] = []
            st.session_state['chat_input_key'] += 1 # Increment key to clear input
            # Ensure the chat input value for the old key is cleared immediately
            if f'user_question_input_{st.session_state["chat_input_key"] - 1}' in st.session_state:
                st.session_state[f'user_question_input_{st.session_state["chat_input_key"] - 1}'] = ""


            if process_pdf_for_rag(uploaded_file):
                st.session_state['pdf_processed'] = True
                st.session_state['faiss_index_ready'] = True
                st.rerun()
            else:
                st.error("Failed to process PDF. Please check the error message above and your Streamlit Cloud logs.")
        else:
            st.info(f"'{uploaded_file.name}' is already processed. You can re-process it if needed.")

with tab2:
    st.header("Ask ESG Questions")

    if not st.session_state['faiss_index_ready']:
        st.warning("Please upload and process an ESG PDF document in the 'Upload & Score' tab first to enable RAG functionality.")
    else:
        st.info("The chatbot is ready to answer questions based on your uploaded document!")

    for i, message in enumerate(st.session_state['chat_history']):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Define the key for the current chat input
    current_chat_input_key = f"user_question_input_{st.session_state['chat_input_key']}"

    # Get the user's question. Streamlit automatically stores its value in st.session_state[key]
    user_question = st.chat_input(
        "Enter your question:",
        key=current_chat_input_key,
        disabled=not st.session_state['faiss_index_ready']
    )

    response_mode = st.radio(
        "Select Response Mode:",
        ('Concise', 'Detailed'),
        horizontal=True,
        key="response_mode_radio"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        # The 'Get Answer' button is clicked OR the user pressed Enter in chat_input
        # We check if user_question has a value AND if it's not already processed
        if st.button("Get Answer", key="get_answer_button", disabled=not st.session_state['faiss_index_ready']) or \
           (user_question and user_question != st.session_state.get(current_chat_input_key + "_processed", "")):
            
            # Use the value directly from st.session_state as soon as the input is submitted
            question_to_process = st.session_state.get(current_chat_input_key, "")

            if question_to_process:
                # Mark this question as processed to avoid double processing on rerun
                st.session_state[current_chat_input_key + "_processed"] = question_to_process

                st.session_state['chat_history'].append({"role": "user", "content": question_to_process})
                with st.spinner("Getting answer..."):
                    try:
                        print(f"DEBUG APP: Attempting to call answer_with_rag for query: '{question_to_process}' in mode: '{response_mode}'")
                        response = answer_with_rag(
                            query=question_to_process,
                            mode=response_mode,
                            index_path=FAISS_INDEX_PATH
                        )
                        print(f"DEBUG APP: Received response from answer_with_rag: {response[:100]}...")
                        st.session_state['chat_history'].append({"role": "assistant", "content": response})
                        
                        # Clear the chat input by incrementing its key and setting its value
                        st.session_state['chat_input_key'] += 1
                        st.session_state[f"user_question_input_{st.session_state['chat_input_key']}"] = "" # Set new key's value to empty
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"An error occurred while getting the answer: {e}")
                        print(f"DEBUG APP: Full error during answer_with_rag call: {e}")
                        st.warning("This could be due to an invalid API key, network issues, or a problem with the RAG chain. Check your Streamlit Cloud logs for more details.")
            else:
                st.warning("Please enter a question.")
    with col2:
        if st.button("Clear Chat History", key="clear_history_button"):
            st.session_state['chat_history'] = []
            st.session_state['chat_input_key'] += 1 # Increment key to clear chat_input widget
            # Ensure the chat input value for the old key is cleared immediately
            if f'user_question_input_{st.session_state["chat_input_key"] - 1}' in st.session_state:
                st.session_state[f'user_question_input_{st.session_state["chat_input_key"] - 1}'] = ""
            st.success("Chat history cleared!")
            st.rerun()

with tab3:
    st.header("ESG Alerts")
    st.write("Click the button below to generate a summary of ESG alerts using your Groq-based alert system.")

    if st.button("Generate ESG Alerts Summary", key="generate_alerts_button"):
        with st.spinner("Generating alerts summary..."):
            try:
                print("DEBUG APP: Attempting to call fetch_esg_alerts...")
                alert_summary_list = fetch_esg_alerts()
                print(f"DEBUG APP: Received alerts: {alert_summary_list}")
                st.subheader("Generated ESG Alert Summary:")
                if alert_summary_list:
                    for item in alert_summary_list:
                        st.markdown(f"- {item}")
                else:
                    st.info("No alerts generated or found.")
            except Exception as e:
                st.error(f"Error generating alerts: {e}")
                print(f"DEBUG APP: Full error during fetch_esg_alerts call: {e}")
                st.warning("Ensure your alerts.py logic is correctly integrated and any required API keys are configured.")

