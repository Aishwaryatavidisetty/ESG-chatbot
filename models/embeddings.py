from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import CohereEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()  # Make sure env variables are loaded

def embed_documents(texts, index_path='vector_store/faiss_index'):
    docs = [Document(page_content=t) for t in texts]

    # ✅ Don't pass the key manually
    embeddings = CohereEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)
