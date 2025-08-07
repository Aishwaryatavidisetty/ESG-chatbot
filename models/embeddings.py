from langchain_community.embeddings import CohereEmbeddings
from langchain.vectorstores import FAISS
from config import COHERE_API_KEY
import os

def embed_documents(texts, index_path='vector_store/faiss_index'):
    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-english-light-v3.0",
        user_agent="esg-chatbot"
    )
    db = FAISS.from_texts(texts, embedding=embeddings)
    db.save_local(index_path)


def load_vectorstore(index_path='vector_store/faiss_index'):
    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-english-light-v3.0",
        user_agent="esg-chatbot"
    )
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)