import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import csv
import json
import spacy # type: ignore
from src.rag.retriever import return_context_by_video_ids
from scripts.topic_lookup import get_video_ids_by_topic
from collections import Counter
from scripts.topic_lookup import get_topics, get_video_ids_by_topic
from src.rag.retriever import return_context_by_video_ids

nlp = spacy.load("de_core_news_sm")

TOP_N = 25
EXAMPLE_MAX_CHARS = 200

# Difficulty levels (example: a1=easy, a2=medium, b1+=hard)
# def word_level(word: str):
#     if len(word) <= 4:
#         return "a1"
#     elif len(word) <= 7:
#         return "a2"
#     else:
#         return "b1"

dataset = {}
topics = get_topics()

for topic in topics:
    print(f"Processing topic: {topic}")

    # Retrieve text from ChromaDB
    video_ids = get_video_ids_by_topic(topic)
    context = return_context_by_video_ids(
        query=topic,
        video_ids=video_ids,
        k=5
    )

    if not context.strip():
        print(f"No context found for {topic}")
        dataset[topic] = []
        continue

    # NLP processing
    doc = nlp(context)

    # Filter: keep nouns, verbs, adjectives; remove stopwords and very short words
    words = [
        token.text for token in doc
        if token.pos_ in ["NOUN", "VERB", "ADJ"]
        and not token.is_stop
        and len(token.text) > 1
    ]

    # Special handling for Alphabet topic: skip single letters
    if topic.lower() == "alphabet":
        words = [w for w in words if len(w) > 1]

    # Count frequency
    freq = Counter(words)
    top_words = [w for w, _ in freq.most_common(TOP_N)]

    vocab_list = []
    for w in top_words:
        # Find first sentence containing the word
        example = next((sent.text for sent in doc.sents if w in sent.text), "")
        # Shorten example for flashcard
        example = example[:EXAMPLE_MAX_CHARS] + "…" if len(example) > EXAMPLE_MAX_CHARS else example

        vocab_list.append({
            "word": w,
            "meaning": "",  # can fill later manually or via dictionary
            "example": example,
            "level": "a1"
        })

    dataset[topic] = vocab_list

# Save to JSON
with open("data/topics_vocab.json", "w", encoding="utf8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("Vocabulary dataset created successfully!")