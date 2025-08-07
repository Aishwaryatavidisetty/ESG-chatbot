from models.llm import load_llm

def google_search(query):
    llm = load_llm()
    prompt = f"Search the web and summarize 3 recent results for: {query}"
    result = llm.invoke(prompt)
    return result.content
