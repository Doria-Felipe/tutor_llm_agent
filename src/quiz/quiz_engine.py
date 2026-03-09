import json
import random
from src.quiz.answer_checker import check_answer
from src.utils.text_normalization import normalize


class QuizEngine:

    def __init__(self, path="data/eval_questions.json"):
        with open(path, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

        self.current_question = None
    
    def next_question(self, level=None):

        questions = self.questions

        if level:
            filtered = [
                q for q in questions
                if q.get("level", "").lower() == level.lower()
            ]

            # fallback if no questions exist for that level
            if filtered:
                questions = filtered

        if not questions:
            raise ValueError("No quiz questions available")

        self.current_question = random.choice(questions)

        return self.current_question["question"]


    def check(self, user_answer):

        if self.current_question is None:
            return {
                "correct": False,
                "correct_answer": None,
                "error": "No question generated"
            }

        correct_answer = self.current_question["ground_truth"]

        user_answer = normalize(user_answer)
        correct_answer = normalize(correct_answer)

        is_correct, similarity = check_answer(user_answer, correct_answer)

        return {
            "correct": is_correct,
            "correct_answer": correct_answer,
            "similarity": round(similarity, 3)
        }