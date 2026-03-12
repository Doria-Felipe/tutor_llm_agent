import json
import re


# JSON extraction helper
def extract_json(text: str):
    """JSON extraction helper
    """
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return text


# Chunk long transcripts
def chunk_text(text, chunk_size=1200):
    """Chunk long transcripts
    """
    chunks = []
    words = text.split()

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

# Lesson Generator
def lesson_agent(title, transcript, level, llm):
    """Lesson Generator
    """
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

    # Remove format="json"
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