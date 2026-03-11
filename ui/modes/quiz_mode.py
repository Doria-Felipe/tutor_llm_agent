import streamlit as st
import json
import random
from src.llm.client import get_llm
from src.agent.answer_grader_agent import grade_answer

LESSON_PATH = "data/lessons/grammar_lessons_explained.json"

@st.cache_resource
def load_llm():
    llm = get_llm("qwen2.5:3b", temperature=0)
    return llm

llm = load_llm()

# Load questions
def load_questions():
    """Recovering questions from the lessons
    """
    with open(LESSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    questions = []

    for lesson in lessons.values():

        for ex in lesson.get("exercises", []):

            question = ex.get("exercise")
            answer = ex.get("answer")

            if question and answer:

                questions.append({
                    "question": question,
                    "answer": answer
                })

    random.shuffle(questions)

    return questions

# Session init
def init_session():
    """Start session
    """
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = load_questions()

    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "checked_answer" not in st.session_state:
        st.session_state.checked_answer = False

    if "last_correct" not in st.session_state:
        st.session_state.last_correct = False


# Next question
def next_question():
    """Going to the next question
    """
    st.session_state.quiz_index += 1
    st.session_state.checked_answer = False
    st.session_state.last_correct = False
    st.rerun()

# Run Quiz Mode
def run_quiz(level=None):
    """Run the quiz
    """
    st.title("Grammar Quiz with AI Grading")
    init_session()

    questions = st.session_state.quiz_questions
    idx = st.session_state.quiz_index

    if not questions:
        st.warning("No quiz questions found.")
        return

    if idx >= len(questions):
        st.success(
            f"Quiz finished! Score: {st.session_state.quiz_score}/{len(questions)}"
        )
        if st.button("Restart Quiz"):
            for key in [
                "quiz_questions", "quiz_index", "quiz_score",
                "checked_answer", "last_result"
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        return

    q = questions[idx]

    st.markdown(f"### {q['question']}")

    user_answer = st.text_input("Your answer", key=f"user_answer_{idx}")

    # Check answer using LLM
    if not st.session_state.checked_answer:
        if st.button("Check Answer"):
            st.session_state.last_result = grade_answer(
                q['question'], q['answer'], user_answer,
                llm=llm
            )
            if st.session_state.last_result["score"] == "correct":
                st.session_state.quiz_score += 1
            st.session_state.checked_answer = True
            st.rerun()

    # Show grading feedback
    else:
        result = st.session_state.last_result
        score = result.get("score")
        feedback = result.get("feedback")
        correction = result.get("correction")

        if score == "correct":
            st.success("✅ Correct!")
        elif score == "almost":
            st.warning("⚠️ Almost correct.")
        else:
            st.error("❌ Not correct.")

        st.info(f"Feedback: {feedback}")
        st.info(f"Corrected answer: {correction}")

        if st.button("Next Question"):
            next_question()

    st.progress((idx + 1) / len(questions))