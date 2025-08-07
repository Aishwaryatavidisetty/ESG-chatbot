import streamlit as st
import os
import time
from dotenv import load_dotenv # To load environment variables locally

# --- Custom Module Imports ---
# Adjust these imports based on your exact file structure
try:
    from models.llm import load_llm
    from utils.rag_utils import answer_with_rag
    # Assuming alerts.py is in the utils directory and has a function for alerts
    from utils.alerts import fetch_esg_alerts # Assuming this function exists in alerts.py
    # from utils.firestore_utils import ... # If you need to use Firestore for chat history or persistent PDF data
    # from config.config import GROQ_API_KEY, COHERE_API_KEY, GROQ_MODEL_NAME # Assuming config.py loads these
except ImportError as e:
    st.error(f"Error importing custom modules: {e}. Please ensure your file structure and module names are correct.")
    st.stop() # Stop the app if essential modules cannot be imported

# --- Langchain and PDF Processing Imports ---
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS # Needed for saving the index

# Load environment variables (important for local testing, Streamlit Cloud handles secrets)
load_dotenv()

# --- API Keys (Ensure these are loaded correctly from your config.py) ---
# For local testing, you might need to load them directly here if config.py isn't set up for it.
# In Streamlit Cloud, these should be set as secrets.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not GROQ_API_KEY or not COHERE_API_KEY:
    st.error("API keys for Groq or Cohere are not set. Please ensure GROQ_API_KEY and COHERE_API_KEY are configured in your environment variables or Streamlit secrets.")
    st.stop() # Stop the app if API keys are missing

# --- Constants ---
FAISS_INDEX_PATH = 'vector_store/faiss_index' # Path to store the FAISS index

# --- Helper Functions ---

def process_pdf_for_rag(uploaded_file):
    """
    Processes an uploaded PDF, chunks it, creates embeddings, and saves a FAISS index.
    """
    if uploaded_file is not None:
        st.info(f"Processing '{uploaded_file.name}' for RAG. This might take a moment...")
        try:
            # Save the uploaded file temporarily
            temp_file_path = f"./temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Load the PDF document
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(documents)

            # Create embeddings
            embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, model="embed-english-light-v3.0")

            # Create FAISS index from documents and save it locally
            st.info("Creating FAISS index...")
            db = FAISS.from_documents(texts, embeddings)
            os.makedirs(FAISS_INDEX_PATH, exist_ok=True) # Ensure directory exists
            db.save_local(FAISS_INDEX_PATH)

            st.success(f"'{uploaded_file.name}' processed and FAISS index created successfully! You can now ask questions.")
            st.warning("Note: In Streamlit Cloud, this index is stored on an ephemeral filesystem and will be lost if the app restarts. For persistent storage, consider using cloud storage (e.g., Google Cloud Storage) or a dedicated vector database.")

            # Clean up the temporary file
            os.remove(temp_file_path)

            return True
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
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

# Check if FAISS index already exists (e.g., from a previous run in the same session)
if os.path.exists(FAISS_INDEX_PATH) and not st.session_state['faiss_index_ready']:
    st.session_state['faiss_index_ready'] = True
    st.session_state['pdf_processed'] = True # Assume PDF was processed if index exists
    st.info("FAISS index found from a previous session. Ready to chat!")


# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Upload & Score", "Chat Interface", "ESG Alerts"])

with tab1:
    st.header("Upload & Score ESG Documents")
    st.write("Upload your ESG PDF document here to enable the chatbot to answer questions based on its content.")
    uploaded_file = st.file_uploader("Upload your ESG PDF document", type="pdf", key="pdf_uploader")

    if uploaded_file:
        if not st.session_state['pdf_processed'] or st.button("Re-process this PDF", key="reprocess_button"):
            # Clear previous state if re-processing
            st.session_state['pdf_processed'] = False
            st.session_state['faiss_index_ready'] = False
            st.session_state['chat_history'] = [] # Clear chat history on re-processing

            if process_pdf_for_rag(uploaded_file):
                st.session_state['pdf_processed'] = True
                st.session_state['faiss_index_ready'] = True
                st.experimental_rerun() # Rerun to update state and UI
            else:
                st.error("Failed to process PDF.")
        else:
            st.info(f"'{uploaded_file.name}' is already processed. You can re-process it if needed.")

with tab2:
    st.header("Ask ESG Questions")

    if not st.session_state['faiss_index_ready']:
        st.warning("Please upload and process an ESG PDF document in the 'Upload & Score' tab first to enable RAG functionality.")
    else:
        st.info("The chatbot is ready to answer questions based on your uploaded document!")

    # Display chat history
    for i, message in enumerate(st.session_state['chat_history']):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Enter your question:", key="user_question_input", disabled=not st.session_state['faiss_index_ready'])

    # Toggle for response mode
    response_mode = st.radio(
        "Select Response Mode:",
        ('Concise', 'Detailed'),
        horizontal=True,
        key="response_mode_radio"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Get Answer", key="get_answer_button", disabled=not st.session_state['faiss_index_ready']):
            if user_question:
                st.session_state['chat_history'].append({"role": "user", "content": user_question})
                with st.spinner("Getting answer..."):
                    try:
                        # Call your actual RAG utility
                        # The 'user_agent' error might be related to the underlying Groq/Cohere client.
                        # Ensure your API keys are correct and network is stable.
                        response = answer_with_rag(
                            query=user_question,
                            mode=response_mode, # Pass 'Concise' or 'Detailed'
                            index_path=FAISS_INDEX_PATH
                        )
                        st.session_state['chat_history'].append({"role": "assistant", "content": response})
                        st.experimental_rerun() # Rerun to display new message
                    except Exception as e:
                        st.error(f"An error occurred while getting the answer: {e}")
                        st.warning("This could be due to an invalid API key, network issues, or a problem with the FAISS index. Check your Streamlit Cloud logs for more details.")
            else:
                st.warning("Please enter a question.")
    with col2:
        if st.button("Clear Chat History", key="clear_history_button"):
            st.session_state['chat_history'] = []
            st.success("Chat history cleared!")
            st.experimental_rerun() # Rerun to clear display

with tab3:
    st.header("ESG Alerts")
    st.write("Click the button below to generate a summary of ESG alerts using your Groq-based alert system.")

    if st.button("Generate ESG Alerts Summary", key="generate_alerts_button"):
        with st.spinner("Generating alerts summary..."):
            try:
                # Call your actual alert generation function from alerts.py
                # Make sure 'generate_alert_summary' is imported from alerts.py
                alert_summary = generate_alert_summary()
                st.subheader("Generated ESG Alert Summary:")
                st.write(alert_summary)
            except Exception as e:
                st.error(f"Error generating alerts: {e}")
                st.warning("Ensure your alerts.py logic is correctly integrated and any required API keys are configured.")

