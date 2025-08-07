from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import CohereEmbeddings
from models.llm import load_llm
from config.config import COHERE_API_KEY # Assuming this is loaded in app.py and passed to CohereEmbeddings
import os

def answer_with_rag(query, mode="Concise", index_path='vector_store/faiss_index'):
    print(f"DEBUG: Entering answer_with_rag for query: '{query}', mode: '{mode}'")
    try:
        # Load LLM
        print(f"DEBUG: Loading LLM with mode: {mode}")
        llm = load_llm(mode)
        print(f"DEBUG: LLM loaded successfully: {llm.model_name}")

        # Ensure FAISS index exists
        if not os.path.exists(index_path):
            error_msg = f"ERROR: FAISS index not found at '{index_path}'. Please ensure a PDF has been processed."
            print(error_msg)
            return error_msg

        # Load Embeddings and FAISS DB
        print("DEBUG: Initializing Cohere Embeddings for FAISS loading...")
        # Ensure COHERE_API_KEY is accessible here, either via config.py or os.getenv
        # For robustness, let's get it directly from env if config.py isn't passing it
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            error_msg = "ERROR: COHERE_API_KEY is not set in environment for CohereEmbeddings in rag_utils.py."
            print(error_msg)
            return error_msg

        embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key, model="embed-english-light-v3.0")
        print(f"DEBUG: Loading FAISS index from '{index_path}'...")
        db = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("DEBUG: FAISS index loaded successfully.")

        # Setup Retriever and QA Chain
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        print("DEBUG: Retriever created. Setting up RetrievalQA chain...")
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        print("DEBUG: RetrievalQA chain created. Running query...")

        # Run the QA chain
        response = qa_chain.run(query)
        print(f"DEBUG: Query executed. Raw response from chain (first 100 chars): {response[:100]}...")
        return response

    except Exception as e:
        error_msg = f"ERROR in answer_with_rag: {e}"
        print(f"DEBUG: {error_msg}")
        # Return a user-friendly error message if an exception occurs
        return f"I encountered an error while trying to answer your question: {e}. Please check the logs for more details."

