import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/entries.csv")

TOPIC_RULES = {
    "Verbs": ["verbs", "sein", "gehen", "fahren", "finden", "geben", "wissen", "machen", "haben", "können", "wollen", "mögen"],
    "Cases": ["case", "cases", "nominativ", "akkusativ", "accusative", "dative"],
    "Prepositions": ["preposition", "präpositionen", "mit", "bei", "ohne"],
    "Restaurant & Food": ["restaurant", "order", "coffee", "drinks", "breakfast", "lunch", "dinner"],
    "Daily Life": ["daily", "morning", "vacation", "winter", "berlin"],
    "Shopping": ["supermarket", "shopping", "grocery", "mall"],
    "Conversation": ["conversation", "small talk", "phrases", "greetings"],
    "Grammar": ["conjugation", "plural", "tense", "imperative"],
    "Vocabulary": ["vocabulary", "fruits", "clothing", "emotions"]
}

def assign_topic(title: str):
    """Function to assign a topic due to a video title

    Args:
        title (str): The video title from the dataset

    Returns:
        _type_: It return the topic of the title
    """
    title_lower = title.lower()

    for topic, keywords in TOPIC_RULES.items():
        if any(k in title_lower for k in keywords):
            return topic

    return "Other"

def main():
    """Add topics to the titles
    """
    df = pd.read_csv(CSV_PATH)

    df["topic"] = df["title"].apply(assign_topic)

    df.to_csv(CSV_PATH, index=False)
    print("Topics assigned successfully.")

if __name__ == "__main__":
    main()