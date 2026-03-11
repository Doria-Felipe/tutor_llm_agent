import re
import pandas as pd
from pathlib import Path
from src.rag.retriever import return_context_by_video_ids

CSV_PATH = Path("data/raw/entries.csv")

def get_grammar_topics():
    df = pd.read_csv(CSV_PATH)
    if "topic" not in df.columns:
        return []
    return sorted(df["topic"].dropna().unique().tolist())

def get_examples_by_topic(topic: str, k=8):
    """
    Pull top-k transcript chunks from ChromaDB for a given topic
    """
    df = pd.read_csv(CSV_PATH)
    video_ids = df[df["topic"] == topic]["id"].tolist()

    if not video_ids:
        return []

    # Pull transcript chunks from ChromaDB
    context = return_context_by_video_ids(query=topic, video_ids=video_ids, k=k)

    # Split by sentence and return top-k
    sentences = re.split(r'(?<=[.!?])\s+', context.strip())
    return sentences[:k]