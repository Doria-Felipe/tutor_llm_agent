import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from src.agent.eval_question_agent import eval_question_agent
from src.llm.ollama_client import get_llm


LESSON_FILE = "data/grammar_lessons_explained.json"
OUTPUT_FILE = "data/eval_questions.json"


llm = get_llm("llama3.1")


with open(LESSON_FILE, encoding="utf8") as f:
    lessons = json.load(f)


dataset = []

for title, lesson in lessons.items():

    print("Generating eval questions for:", title)

    questions = eval_question_agent(
        lesson=lesson,
        llm=llm
    )

    for q in questions:

        q["topic"] = title
        dataset.append(q)


Path("data").mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("✅ Evaluation dataset created")
print("Total questions:", len(dataset))