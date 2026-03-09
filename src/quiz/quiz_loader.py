import json

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_quiz():
    manual = load_json("data/eval_questions.json")
    generated = load_json("data/generated_quizzes.json")
    return manual + generated