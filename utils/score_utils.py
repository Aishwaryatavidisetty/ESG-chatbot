def calculate_esg_scores(text):
    keywords = {
        "Environmental": ["carbon", "renewable", "emissions", "climate", "energy"],
        "Social": ["diversity", "inclusion", "health", "safety", "training"],
        "Governance": ["board", "compliance", "audit", "transparency", "ethics"]
    }
    scores = {}
    for category, words in keywords.items():
        count = sum(text.lower().count(word) for word in words)
        scores[category] = count
    total = sum(scores.values()) or 1
    for cat in scores:
        scores[cat] = round((scores[cat] / total) * 100, 2)
    return scores


