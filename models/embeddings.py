from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config.config import GROQ_API_KEY 

def embed_documents(texts, index_path='vector_store/faiss_index'):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)
    embeddings = OpenAIEmbeddings(openai_api_key=GROQ_API_KEY)  # or your OpenAI key
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)

