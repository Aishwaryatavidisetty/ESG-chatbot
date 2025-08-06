from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from models.llm import load_llm

def answer_with_rag(query, index_path='vector_store/faiss_index'):
    llm = load_llm()
    db = FAISS.load_local(
        index_path,
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True  # ✅ This enables loading trusted local pickle
    )
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(query)
