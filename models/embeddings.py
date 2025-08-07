from langchain_community.embeddings import CohereEmbeddings
from langchain.vectorstores import FAISS
from config import COHERE_API_KEY

def embed_documents(texts, index_path='vector_store/faiss_index'):
    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model='embed-english-light-v3.0',
        user_agent="esg-chatbot"
    )
    db = FAISS.from_texts(texts, embedding=embeddings)
    db.save_local(index_path)
