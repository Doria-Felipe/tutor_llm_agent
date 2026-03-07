import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from src.llm.ollama_client import get_llm
from src.agent.lesson_explainer_agent import lesson_explainer_agent


INPUT_FILE = "data/grammar_lessons.json"
OUTPUT_FILE = "data/grammar_lessons_explained.json"


llm = get_llm("llama3.1")


with open(INPUT_FILE, encoding="utf8") as f:
    lessons = json.load(f)


expanded = {}

for title, lesson in lessons.items():

    print(f"Expanding lesson: {title}")

    explained = lesson_explainer_agent(
        lesson=lesson,
        llm=llm
    )

    expanded[title] = explained


Path("data").mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(expanded, f, ensure_ascii=False, indent=2)

print("\n✅ Lessons expanded!")