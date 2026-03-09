import streamlit as st
from src.quiz.quiz_engine import QuizEngine


def run_quiz(level):

    st.title("German Learning Quiz 🇩🇪")

    if "quiz" not in st.session_state:
        st.session_state.quiz = QuizEngine()

    if st.button("New Question"):

        q = st.session_state.quiz.next_question(level)

        st.session_state.question = q

    if "question" not in st.session_state:
        st.session_state.question = st.session_state.quiz.next_question(level)

    if "question" in st.session_state:

        st.markdown("### Question")
        st.write(st.session_state.question)

        answer = st.text_input("Your answer")

        if st.button("Submit"):

            result = st.session_state.quiz.check(answer)

            if result.get("error"):
                st.warning("Generate a question first.")
                return

            if result["correct"]:
                st.success("Correct! 🎉")
            else:
                # st.error("Not quite.")
                st.error("Not quite.")
                st.caption(f"Similarity score: {result['similarity']}")

            st.write("Correct answer:", result["correct_answer"])