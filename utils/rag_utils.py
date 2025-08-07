from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import CohereEmbeddings
from config import COHERE_API_KEY
from models.llm import load_llm


def answer_with_rag(query, index_path='vector_store/faiss_index', mode='concise'):
    llm = load_llm()
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt": None})
    return chain.run(query)