import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import re
from src.rag.vector_store import col
from llm.client import get_llm

# -------------------------------
# Safe Quiz Generator using llm.invoke
# -------------------------------
llm = get_llm("llama3.1")  # returns your Ollama LLM object


PROMPT_TEMPLATE = """
You are creating German learning quiz questions.

From the transcript segment below, generate ONE quiz question.

Rules:
- Return ONLY valid JSON (no extra text)
- Use double quotes
- Must have "question" and "answer" keys

Transcript:
{chunk}

Return example:
{{"question": "How do you say ...", "answer": "Ich ..."}}
"""


def generate_quiz(chunk: str) -> dict:
    """Generate a single quiz question from a transcript chunk."""
    prompt = PROMPT_TEMPLATE.format(chunk=chunk)

    # Call the LLM safely
    response_obj = llm.invoke(prompt)

    # Extract the text — handle different return types (AIMessage, str, dict)
    if hasattr(response_obj, "content"):  # AIMessage object
        text = response_obj.content
    elif isinstance(response_obj, str):
        text = response_obj
    else:
        raise ValueError(f"Unexpected LLM return type: {type(response_obj)}")

    text = text.strip()

    # Parse JSON safely
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract JSON from text using regex
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from LLM output:\n{text}")


# -------------------------------
# Generate quizzes from Chroma DB
# -------------------------------
docs = col.get(include=["documents", "metadatas"])

questions = []

for doc, meta in zip(docs["documents"], docs["metadatas"]):
    try:
        q = generate_quiz(doc)

        # Attach metadata
        q["video_id"] = meta.get("video_id")
        q["start"] = meta.get("start")
        q["difficulty"] = "A1"  # optional: later detect from content
        questions.append(q)
    except Exception as e:
        print("Skipping chunk:", e)
        continue

# Save all generated questions
with open("data/generated_quizzes.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Generated {len(questions)} quiz questions!")