from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import CohereEmbeddings
from models.llm import load_llm
from config.config import COHERE_API_KEY

def answer_with_rag(query, mode="Concise", index_path='vector_store/faiss_index'):
    llm = load_llm(mode)  # Pass mode to load_llm so it can pick model accordingly
    db = FAISS.load_local(
        index_path,
        CohereEmbeddings(model="embed-english-light-v3.0"),
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(query)