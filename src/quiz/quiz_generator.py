import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from src.llm.ollama_client import get_llm  # your existing LLM loader
import re

# Load the LLM once
llm = get_llm("llama3.1")  # returns an object that supports .invoke(prompt)

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
    """Generate a single quiz question from a transcript chunk"""
    prompt = PROMPT_TEMPLATE.format(chunk=chunk)

    # Use llm.invoke() instead of calling the object
    text = llm.invoke(prompt).strip()

    # Attempt to parse JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract JSON from text using regex
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from LLM output:\n{text}")