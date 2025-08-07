from models.llm import load_llm

def google_search(query):
    llm = load_llm()
    prompt = f"Give 3 recent search results with title and link for the query: {query}"
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error fetching search from LLM: {e}"