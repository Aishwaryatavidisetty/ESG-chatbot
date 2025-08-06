from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import streamlit as st  # ✅ Needed for st.secrets

def embed_documents(texts, index_path='vector_store/faiss_index'):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)

    # ✅ Use Streamlit secrets
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)
