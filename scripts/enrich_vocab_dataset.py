import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
# from src.llm.ollama_client import get_llm
from src.llm.local_vllm_client import get_llm
from src.agent.german_agent import german_agent

llm = get_llm("llama3.1", temperature=0)

with open("data/topics_vocab.json", "r", encoding="utf8") as f:
    dataset = json.load(f)


def clean_json(response):
    response = response.strip()

    if "```" in response:
        response = response.split("```")[1]
        response = response.replace("json", "").strip()

    return response


for topic, words in dataset.items():

    print(f"Enriching topic: {topic}")

    for entry in words:

        word = entry["word"]
        context = entry["example"]

        prompt = f"""
You are helping build German vocabulary flashcards.

WORD:
{word}

TRANSCRIPT:
{context}

TASK:
1. Give a short English meaning (max 5 words).
2. Extract ONE clean German sentence from the transcript that contains the word "{word}".
3. If the transcript sentence is messy, rewrite it into a natural short sentence.

RULES:
- Sentence must contain the word "{word}"
- Maximum 12 words
- A1 learner friendly
- Output ONLY JSON

FORMAT:
{{
  "meaning": "...",
  "example": "..."
}}
"""

        response = german_agent(
            llm=llm,
            user_query=prompt,
            ctx=context,
            mode="vocab",
            level="a1"
        )

        try:
            parsed = json.loads(clean_json(response))

            entry["meaning"] = parsed.get("meaning", "")
            entry["example"] = parsed.get("example", "")

        except json.JSONDecodeError:
            print(f"Failed to parse JSON for word '{word}' in topic '{topic}'")
            print("Raw response:", response)


with open("data/topics_vocab_enriched.json", "w", encoding="utf8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("Vocabulary enrichment complete.")