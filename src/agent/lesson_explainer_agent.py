import json
import re

def extract_json(text: str):
    """JSON extraction helper
    """
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return text

def lesson_explainer_agent(lesson, llm):
    """
    Enhance the lesson JSON:
    - Add learner-friendly grammar notes
    - Add optional exercises
    - Ensure bilingual examples
    """
    prompt = f"""
        You are an expert German teacher.

        Expand the following A1 lesson for students:

        {json.dumps(lesson, ensure_ascii=False)}

        Output JSON format:

        {{
        "title": "lesson title",
        "vocabulary": [
            {{"word": "...", "translation": "...", "note": "..."}}
        ],
        "examples": [
            {{"german": "...", "english": "...", "note": "..."}}
        ],
        "grammar_notes": [
            "...", "..."
        ],
        "exercises": [
            "...", "..."
        ]
        }}

        Rules:
        - Keep max 5 vocab words and 5 examples
        - Include simple notes explaining tricky parts
        - JSON only, no markdown, complete and valid
        """

    response = llm.invoke(prompt)
    raw = response.content

    try:
        clean_json = extract_json(raw)
        return json.loads(clean_json)
    
    except Exception as e:
        print("\nRAW LLM OUTPUT:\n", raw)
        # fallback safe output
        return {
            "title": lesson.get("title","unknown"),
            "vocabulary": lesson.get("vocabulary", []),
            "examples": lesson.get("examples", []),
            "grammar_notes": [],
            "exercises": []
        }