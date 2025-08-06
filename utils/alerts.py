import requests
import os

def fetch_esg_alerts():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    query = "latest ESG regulations 2025"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    try:
        response = requests.get(url)
        results = response.json().get("items", [])
        alerts = []
        for item in results[:5]:
            alerts.append(f"**{item['title']}**\n🔗 {item['link']}")
        return alerts
    except Exception as e:
        return [f"Error fetching alerts: {e}"]
