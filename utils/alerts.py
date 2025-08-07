from models.llm import load_llm

def fetch_esg_alerts():
    try:
        llm = load_llm()
        prompt = "List the latest 5 ESG regulation updates or news in 2025 with sources."
        result = llm.invoke(prompt)
        return [result.content]
    except Exception as e:
        return [f"Error fetching alerts from LLM: {e}"]
