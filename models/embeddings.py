from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config.config import OPENAI_API_KEY  # Assuming you stored your OpenAI key as this

def embed_documents(texts, index_path='vector_store/faiss_index'):
    # Split long texts into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)

    # Create embeddings using your OpenAI key
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Create and store FAISS vector index
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)
