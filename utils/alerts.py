from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from config.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-70b-8192",  # ✅ Fix here
)

def fetch_esg_alerts():
    try:
        messages = [HumanMessage(content="Get latest ESG news or regulation updates (2025). Respond briefly.")]
        response = llm.invoke(messages)
        return [response.content]
    except Exception as e:
        return [f"Error fetching alerts from LLM: {e}"]
