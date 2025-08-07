def calculate_esg_scores(text):
    text_lower = text.lower()
    environmental_keywords = ["emissions", "carbon", "climate", "waste", "pollution"]
    social_keywords = ["diversity", "inclusion", "labor", "safety", "community"]
    governance_keywords = ["compliance", "board", "ethics", "transparency", "audit"]

    def score(keywords):
        return sum(1 for word in keywords if word in text_lower) / len(keywords) * 100

    return {
        "Environmental": score(environmental_keywords),
        "Social": score(social_keywords),
        "Governance": score(governance_keywords),
    }
