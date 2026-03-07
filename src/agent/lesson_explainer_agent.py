import json
import re


def extract_json(text: str):

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return text


def lesson_explainer_agent(lesson, llm):

    prompt = f"""
You are a German teacher.

Expand this lesson so it becomes a **complete beginner lesson**.

Lesson:

{json.dumps(lesson, ensure_ascii=False, indent=2)}

Return ONLY valid JSON.

Format:

{{
"title": "...",

"grammar_explanation": "...",

"vocabulary":[
{{
"word":"...",
"translation":"...",
"explanation":"..."
}}
],

"examples":[
{{
"german":"...",
"english":"...",
"explanation":"Explain grammar of the sentence."
}}
]
}}

Rules:
- Grammar explanation must be simple (A1 level)
- Explain vocabulary meaning and usage
- Explain grammar of the example sentences
- Keep explanations short
- JSON only
"""

    response = llm.invoke(prompt)

    raw = response.content

    try:
        clean_json = extract_json(raw)
        return json.loads(clean_json)

    except Exception:

        print("\nRAW LLM OUTPUT:\n", raw)

        return lesson