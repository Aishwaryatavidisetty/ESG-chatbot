from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_cohere import CohereEmbeddings
from models.llm import load_llm
from config.config import COHERE_API_KEY

def answer_with_rag(query, index_path='vector_store/faiss_index'):
    llm = load_llm()
    db = FAISS.load_local(
        index_path,
        CohereEmbeddings(cohere_api_key=COHERE_API_KEY),
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(query)