import json
import re

INPUT_FILE = "data/topics_vocab_enriched.json"
OUTPUT_FILE = "data/vocab/topics_vocab_clean.json"


def normalize(text):
    """Lowercase + remove punctuation for matching."""
    return re.sub(r"[^\wäöüß]", "", text.lower())


def example_contains_word(word, example):
    """Check if word exists in example."""
    w = normalize(word)
    tokens = [normalize(t) for t in example.split()]
    return w in tokens


def repair_example(word, example):
    """
    Try to repair example by inserting the word.
    """

    if not example:
        return f"Das Wort ist '{word}'."

    # If example too generic, rebuild
    if len(example.split()) < 3:
        return f"Ich benutze das Wort {word}."

    # Otherwise prepend word
    return f"{word.capitalize()} ist ein deutsches Wort."

# Cleaning the messy dataset examples
def clean_dataset(data):
    """
    Cleaning the dataset examples.
    """

    fixed = {}

    for topic in data:

        fixed[topic] = []

        for entry in data[topic]:

            word = entry["word"].strip()
            example = entry.get("example", "")

            if example_contains_word(word, example):

                fixed[topic].append(entry)

            else:

                repaired = repair_example(word, example)

                entry["example"] = repaired
                fixed[topic].append(entry)

    return fixed


def main():

    with open(INPUT_FILE, encoding="utf8") as f:
        data = json.load(f)

    cleaned = clean_dataset(data)

    with open(OUTPUT_FILE, "w", encoding="utf8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print("Clean dataset written to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()