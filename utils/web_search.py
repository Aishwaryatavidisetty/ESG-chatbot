import os
import requests
from config.config import GOOGLE_API_KEY, GOOGLE_CX


def google_search(query):
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    response = requests.get(url)
    results = response.json().get("items", [])
    return "\n".join([item['title'] + "\n" + item['link'] for item in results[:3]])