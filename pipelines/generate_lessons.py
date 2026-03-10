import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import chromadb
from src.llm.client import get_llm
from src.agent.lesson_agent import lesson_agent
from src.agent.lesson_explainer_agent import lesson_explainer_agent

# -----------------------------
# Config
# -----------------------------
DB_PATH = "./chroma_easy_german"
COLLECTION_NAME = "easy_german_a1_multi"
RAW_OUTPUT_FILE = "data/grammar_lessons.json"
EXPLAINED_OUTPUT_FILE = "data/grammar_lessons_explained.json"
LLM_MODEL = "llama3.1"

# -----------------------------
# Load ChromaDB
# -----------------------------
client = chromadb.PersistentClient(path=DB_PATH)
col = client.get_or_create_collection(COLLECTION_NAME)

res = col.get(include=["documents","metadatas"])
docs = res["documents"]
metas = res["metadatas"]

videos = {}
for doc, meta in zip(docs, metas):
    title = meta.get("title", "unknown")
    text = doc[0] if isinstance(doc, list) else doc
    videos.setdefault(title, []).append(text)

# -----------------------------
# Initialize LLM
# -----------------------------
llm = get_llm(LLM_MODEL)

# -----------------------------
# Generate raw lessons
# -----------------------------
lessons = {}
for title, chunks in videos.items():
    transcript = " ".join(chunks)
    print(f"Generating raw lesson: {title}")
    lesson = lesson_agent(title=title, transcript=transcript, level="a1", llm=llm)
    lessons[title] = lesson

Path("data").mkdir(exist_ok=True)
with open(RAW_OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
print(f"✅ Raw grammar lessons saved to {RAW_OUTPUT_FILE}")

# -----------------------------
# Generate explained lessons
# -----------------------------
explained_lessons = {}
for title, lesson in lessons.items():
    print(f"Expanding lesson: {title}")
    explained = lesson_explainer_agent(lesson=lesson, llm=llm)
    explained_lessons[title] = explained

with open(EXPLAINED_OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(explained_lessons, f, ensure_ascii=False, indent=2)
print(f"✅ Explained grammar lessons saved to {EXPLAINED_OUTPUT_FILE}")