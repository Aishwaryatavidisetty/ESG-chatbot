from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from config.config import COHERE_API_KEY

def embed_documents(docs, index_path="vector_store/faiss_index"):
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, user_agent="esg-chatbot")
    db = FAISS.from_texts(docs, embedding=embeddings)
    db.save_local(index_path)