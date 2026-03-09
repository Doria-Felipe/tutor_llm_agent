# import pandas as pd
# from pathlib import Path

# CSV_PATH = Path("data/entries.csv")

# TOPIC_RULES = {
#     "Verbs": ["verbs", "sein", "gehen", "fahren", "finden", "geben", "wissen", "machen", "haben", "können", "wollen", "mögen"],
#     "Cases": ["case", "cases", "nominativ", "akkusativ", "accusative", "dative"],
#     "Prepositions": ["preposition", "präpositionen", "mit", "bei", "ohne"],
#     "Restaurant & Food": ["restaurant", "order", "coffee", "drinks", "breakfast", "lunch", "dinner"],
#     "Daily Life": ["daily", "morning", "vacation", "winter", "berlin"],
#     "Shopping": ["supermarket", "shopping", "grocery", "mall"],
#     "Conversation": ["conversation", "small talk", "phrases", "greetings"],
#     "Grammar": ["conjugation", "plural", "tense", "imperative"],
#     "Vocabulary": ["vocabulary", "fruits", "clothing", "emotions"]
# }

# def assign_topic(title: str):
#     """Function to assign a topic due to a video title

#     Args:
#         title (str): The video title from the dataset

#     Returns:
#         _type_: It return the topic of the title
#     """
#     title_lower = title.lower()

#     for topic, keywords in TOPIC_RULES.items():
#         if any(k in title_lower for k in keywords):
#             return topic

#     return "Other"

# def main():
#     """Add topics to the titles
#     """
#     df = pd.read_csv(CSV_PATH)

#     df["topic"] = df["title"].apply(assign_topic)

#     df.to_csv(CSV_PATH, index=False)
#     print("Topics assigned successfully.")

# if __name__ == "__main__":
#     main()

import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/entries.csv")

# -------------------------
# Hierarchical topic structure
# -------------------------
TOPIC_STRUCTURE = {
    "Verbs": {
        "Common verbs": ["sein", "haben", "gehen", "machen", "wissen", "können", "wollen", "mögen"],
        "Modal verbs": ["dürfen", "müssen", "sollen"],
        "Separable verbs": ["aufstehen", "mitbringen", "anfangen"]
    },
    "Nouns": {
        "Daily life": ["Haus", "Straße", "Morgen", "Abend", "Familie"],
        "Food & Restaurant": ["Kaffee", "Brot", "Milch", "Restaurant", "Mittagessen"],
        "Shopping": ["Supermarkt", "Einkauf", "Kleidung", "Geld"]
    },
    "Grammar": {
        "Cases": ["Nominativ", "Akkusativ", "Dativ", "Genitiv"],
        "Prepositions": ["mit", "bei", "für", "ohne"]
    },
    "Conversation": {
        "Greetings": ["Hallo", "Guten Morgen", "Tschüss"],
        "Small talk": ["Wie geht’s?", "Schönes Wetter"]
    }
}

# -------------------------
# Assign topic based on title
# -------------------------
def assign_topic(title: str) -> str:
    title_lower = title.lower()
    for main_topic, subtopics in TOPIC_STRUCTURE.items():
        for subtopic, keywords in subtopics.items():
            if any(k.lower() in title_lower for k in keywords):
                return f"{main_topic} → {subtopic}"
    return "Other"

# -------------------------
# Main
# -------------------------
def main():
    df = pd.read_csv(CSV_PATH)
    df["topic"] = df["title"].apply(assign_topic)
    df.to_csv(CSV_PATH, index=False)
    print("Topics assigned successfully.")

if __name__ == "__main__":
    main()