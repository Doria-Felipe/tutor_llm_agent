import json
import re


def extract_json(text):

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if match:
        return match.group(0)

    return text


def eval_question_agent(lesson, llm):

    prompt = f"""
You are creating evaluation questions for a German tutor system.

Based on this lesson, generate 3 questions a learner might ask.

Lesson:
{json.dumps(lesson, ensure_ascii=False, indent=2)}

Return ONLY JSON.

Format:

[
 {{
  "question": "...",
  "ground_truth": "..."
 }},
 {{
  "question": "...",
  "ground_truth": "..."
 }},
 {{
  "question": "...",
  "ground_truth": "..."
 }}
]

Rules:
- Questions must be about the grammar or vocabulary in the lesson
- Ground truth must be concise
- Beginner level
- JSON only
"""

    response = llm.invoke(prompt)

    raw = response.content

    try:
        clean = extract_json(raw)
        return json.loads(clean)

    except Exception:

        print("RAW OUTPUT:\n", raw)
        return []