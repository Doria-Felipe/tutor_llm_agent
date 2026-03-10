import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import pandas as pd

from src.rag.retriever import return_context
from src.agent.german_agent import german_agent
# from src.llm.ollama_client import get_llm
from src.llm.local_vllm_client import get_llm

llm = get_llm("llama3.1")


with open("data/eval_questions.json") as f:
    questions = json.load(f)


records = []

for q in questions:

    question = q["question"]

    context = return_context(question, k=3)

    answer = german_agent(
        llm=llm,
        user_query=question,
        ctx=context,
        mode="tutor",
        level="a1"
    )

    records.append({
        "question": question,
        "context": context,
        "answer": answer,
        "ground_truth": q["ground_truth"]
    })


df = pd.DataFrame(records)

df.to_csv("data/generated_answers.csv", index=False)

print(f"Saved {len(df)} generated answers")