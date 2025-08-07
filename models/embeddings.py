from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import CohereEmbeddings
from langchain_core.documents import Document
from config.config import COHERE_API_KEY


def embed_documents(texts, index_path='vector_store/faiss_index'):
    docs = [Document(page_content=text) for text in texts]
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)
