import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import chromadb
from llm.client import get_llm
from src.agent.lesson_agent import lesson_agent

# Configuration
DB_PATH = "./chroma_easy_german"
COLLECTION_NAME = "easy_german_a1_multi"
OUTPUT_FILE = "data/grammar_lessons.json"

llm_model = "llama3.1"

# Initialize ChromaDB
client = chromadb.PersistentClient(path=DB_PATH)
col = client.get_or_create_collection(COLLECTION_NAME)

print("Collections:", [c.name for c in client.list_collections()])

# Get all documents and metadata
res = col.get(include=["documents", "metadatas"])
docs = res["documents"]
metas = res["metadatas"]

videos = {}

for doc, meta in zip(docs, metas):

    title = meta.get("title", "unknown")

    if title not in videos:
        videos[title] = []

    text = doc[0] if isinstance(doc, list) else doc

    videos[title].append(text)

# Fallback IDs
ids = [meta.get("id", f"video_{i}") for i, meta in enumerate(metas)]
print(f"Number of items in collection: {len(ids)}")

# Prepare LLM
llm = get_llm(llm_model)
lessons = {}

# Generate lessons
for title, chunks in videos.items():

    transcript = " ".join(chunks)

    print(f"\nGenerating lesson from video: {title}")

    lesson = lesson_agent(
        title=title,
        transcript=transcript,
        level="a1",
        llm=llm
    )

    lessons[title] = lesson

# Save JSON
Path("data").mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print(f"Grammar lessons saved to {OUTPUT_FILE}")