from models.llm import load_llm

def fetch_esg_alerts():
    llm = load_llm()
    query = "List 3 latest ESG regulation updates (as of 2025) with links"
    try:
        response = llm.invoke(query)
        return response.content.split("\n")
    except Exception as e:
        return [f"Error fetching alerts from LLM: {e}"]