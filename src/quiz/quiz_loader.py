import json
import random


def load_quiz(path="data/eval_questions.json"):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def sample_question(data):

    return random.choice(data)