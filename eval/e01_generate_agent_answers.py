import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import pandas as pd
from tqdm import tqdm

from src.llm.client import get_llm
from src.agent.tools import build_german_tool
from src.rag.hybrid_retriever import return_context

# SETTINGS

LESSONS_PATH = "data/lessons/grammar_lessons_explained.json"
OUTPUT_PATH = "data/eval/generated_agent_answers.csv"

llm = get_llm("llama3.1")
# llm = get_llm("qwen2.5:3b")
agent = build_german_tool(llm, level="a1")

# LOAD LESSON FILE
with open(LESSONS_PATH, "r", encoding="utf-8") as f:
    lessons = json.load(f)

records = []

# EXTRACT EXERCISES
for video_title, lesson in lessons.items():

    exercises = lesson.get("exercises", [])

    for ex in exercises:
        print(f'New question:')
        question = ex.get("exercise") or ex.get("question") or ex.get("prompt")
        ground_truth = ex.get("answer") or ex.get("solution")
        print(f'Q: {question}')

        if not question or not ground_truth:
            continue

        context = return_context(question, k=3)

        answer = agent._run(question)
        print(f'A: {answer}')

        records.append({
            "video": video_title,
            "question": question,
            "answer": answer,
            "ground_truth": ground_truth,
            "context": context
        })

df = pd.DataFrame(records)

df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved {len(df)} generated answers to {OUTPUT_PATH}")