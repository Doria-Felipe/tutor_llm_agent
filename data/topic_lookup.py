import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/entries.csv")

def get_topics():
    """ helper function to get topics from the entries.csv
    """
    df = pd.read_csv(CSV_PATH)
    return sorted(df["topic"].dropna().unique().tolist())

def get_video_ids_by_topic(topic: str):
    df = pd.read_csv(CSV_PATH)
    return df[df["topic"] == topic]["id"].tolist()