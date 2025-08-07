from models.llm import load_llm

def fetch_esg_alerts():
    llm = load_llm()
    prompt = "Give the 5 latest headlines with links about ESG regulations or scandals."
    try:
        response = llm.invoke(prompt)
        return response.content.split("\n")
    except Exception as e:
        return [f"Error fetching alerts from LLM: {e}"]