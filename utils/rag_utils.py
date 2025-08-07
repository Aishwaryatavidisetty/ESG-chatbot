from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_cohere import CohereEmbeddings
from models.llm import load_llm

def answer_with_rag(query, index_path='vector_store/faiss_index', mode="Concise"):
    llm = load_llm(mode=mode)  # pass mode to llm loader if applicable
    db = FAISS.load_local(
        index_path,
        CohereEmbeddings(),
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(query)
