from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_cohere import CohereEmbeddings
from models.llm import load_llm
from config.config import COHERE_API_KEY  # Make sure this is defined in config.py

def answer_with_rag(query, index_path='vector_store/faiss_index'):
    llm = load_llm()

    # Use Cohere embeddings
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)

    # Load FAISS vector store
    db = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Create retriever and QA chain
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(query)
