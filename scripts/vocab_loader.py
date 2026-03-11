import json
from pathlib import Path

VOCAB_PATH = Path("data/vocab/topics_vocab_clean.json")


def load_vocab():
    with open(VOCAB_PATH, encoding="utf8") as f:
        return json.load(f)
