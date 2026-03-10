import json
import re


# -----------------------------
# JSON extraction helper
# -----------------------------
def extract_json(text: str):

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return text


# -----------------------------
# Chunk long transcripts
# -----------------------------
def chunk_text(text, chunk_size=1200):

    chunks = []
    words = text.split()

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# -----------------------------
# Lesson Generator
# -----------------------------

def lesson_agent(title, transcript, level, llm):
    chunks = chunk_text(transcript)
    context = " ".join(chunks[:2])

    prompt = f"""
You are a German teacher.

Create a **short A1 German lesson** based on this transcript.

Video title:
{title}

Transcript:
{context}

Return ONLY valid JSON.

Format:

{{
"title": "lesson title",
"vocabulary": [
{{"word": "Haus", "translation": "house"}},
{{"word": "Baum", "translation": "tree"}}
],
"examples": [
{{"german": "Das Haus ist groß.", "english": "The house is big."}},
{{"german": "Der Baum ist alt.", "english": "The tree is old."}}
]
}}

Rules:
- Maximum 5 vocabulary words
- Maximum 5 examples
- No explanations
- No markdown
- JSON only
- Make sure the JSON is complete and closed.
"""

    # ===========================
    # FIX HERE: remove format="json"
    # ===========================
    response = llm.invoke(prompt)  # just pass the prompt

    raw = response.content

    try:
        clean_json = extract_json(raw)
        return json.loads(clean_json)

    except Exception as e:
        print("\nRAW LLM OUTPUT:\n", raw)
        # Safe fallback
        return {
            "title": title,
            "vocabulary": [],
            "examples": []
        }

# def lesson_agent(title, transcript, level, llm):

#     chunks = chunk_text(transcript)

#     # Use first chunk only (best intro context)
#     # context = chunks[0]
#     context = " ".join(chunks[:2])

#     prompt = f"""
# You are a German teacher.

# Create a **short A1 German lesson** based on this transcript.

# Video title:
# {title}

# Transcript:
# {context}

# Return ONLY valid JSON.

# Format:

# {{
# "title": "lesson title",
# "vocabulary": [
# {{"word": "Haus", "translation": "house"}},
# {{"word": "Baum", "translation": "tree"}}
# ],
# "examples": [
# {{"german": "Das Haus ist groß.", "english": "The house is big."}},
# {{"german": "Der Baum ist alt.", "english": "The tree is old."}}
# ]
# }}

# Rules:
# - Maximum 5 vocabulary words
# - Maximum 5 examples
# - No explanations
# - No markdown
# - JSON only
# - Make sure the JSON is complete and closed.
# """

#     response = llm.invoke(prompt, format="json")

#     raw = response.content

#     try:
#         clean_json = extract_json(raw)
#         return json.loads(clean_json)

#     except Exception as e:

#         print("\nRAW LLM OUTPUT:\n", raw)

#         # Safe fallback so script never crashes
#         return {
#             "title": title,
#             "vocabulary": [],
#             "examples": []
#         }


# import json
# import re

# def extract_json_loose(text: str):
#     """
#     Extract JSON from LLM output, fix unclosed braces or strings.
#     Returns a JSON string as best effort.
#     """

#     # Remove markdown/code blocks
#     text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

#     # Try to find first { ... }
#     match = re.search(r"\{.*", text, re.DOTALL)
#     if match:
#         raw = match.group(0)

#         # Fix unclosed braces
#         open_braces = raw.count("{")
#         close_braces = raw.count("}")
#         if open_braces > close_braces:
#             raw += "}" * (open_braces - close_braces)

#         # Fix unclosed quotes at the end
#         quotes = raw.count('"')
#         if quotes % 2 != 0:
#             raw += '"'

#         return raw

#     return text

# def lesson_agent(title: str, transcript: str, level: str, llm) -> dict:
#     """
#     Generate lesson dict with 'title', 'vocabulary', 'examples'.
#     """

#     prompt = f"""
# Create a short German lesson for level {level} based on this transcript.
# Use **up to 5 vocabulary words** and **up to 5 examples**.

# Video title: {title}

# Transcript:
# {transcript}

# Return ONLY valid JSON:

# {{
#   "title": "lesson title",
#   "vocabulary": [
#     {{"word": "Haus", "translation": "house"}}
#   ],
#   "examples": [
#     {{"german": "Das Haus ist groß.", "english": "The house is big."}}
#   ]
# }}

# Do not include explanations or markdown. Return JSON only.
# """

#     # Call LLM
#     response = llm.invoke(prompt)
#     raw = response.content

#     # Extract and parse
#     try:
#         clean = extract_json_loose(raw)
#         return json.loads(clean)
#     except Exception as e:
#         print("\nRAW LLM OUTPUT:\n", raw)
#         # Attempt minimal fallback: only title + empty lists
#         return {
#             "title": title,
#             "vocabulary": [],
#             "examples": []
#         }