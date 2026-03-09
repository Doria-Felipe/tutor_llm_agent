from src.quiz.quiz_loader import load_quiz
import random

class QuizEngine:
    def __init__(self):
        self.questions = load_quiz()
        self.current_question = None

    def next_question(self, level=None):
        questions = self.questions
        if level:
            filtered = [q for q in questions if q.get("difficulty", "").lower() == level.lower()]
            if filtered:
                questions = filtered
        if not questions:
            raise ValueError("No quiz questions available")
        self.current_question = random.choice(questions)
        return self.current_question["question"]

    def check(self, user_answer):
        if not self.current_question:
            return {"correct": False, "correct_answer": None, "error": "No question generated"}
        correct_answer_raw = self.current_question["answer"]
        from src.utils.text_normalization import normalize
        from src.quiz.answer_checker import check_answer
        user_answer_norm = normalize(user_answer)
        correct_answer_norm = normalize(correct_answer_raw)
        is_correct, similarity = check_answer(user_answer_norm, correct_answer_norm)
        return {
            "correct": is_correct,
            "correct_answer": correct_answer_raw,
            "similarity": round(similarity, 3)
        }