import streamlit as st
import json

LESSON_PATH = "data/lessons/grammar_lessons_explained.json"


# Load lessons
def load_lessons():
    """Populate a JSON with the lessons.
    Returns:
        JSON: the JSON file with enriched lessons.
    """
    with open(LESSON_PATH, encoding="utf-8") as f:
        return json.load(f)


# Vocabulary block
def show_vocab(vocab):
    """The vocabulary from the lesson.
    """
    st.subheader("Vocabulary")

    for v in vocab:

        with st.expander(f"{v['word']} — {v['translation']}"):

            if "note" in v:
                st.write(v["note"])



# Examples
def show_examples(examples):
    """The examples enriched previously
    """
    st.subheader("Examples")

    for ex in examples:

        st.markdown(f"**{ex['german']}**")
        st.markdown(f"{ex['english']}")

        if "note" in ex:
            st.caption(ex["note"])

        st.write("")


# Grammar Notes
def show_grammar(notes):
    """Important notes from the tutor about the subject
    """
    if not notes:
        return

    st.subheader("Grammar Notes")

    for n in notes:
        st.markdown(f"- {n}")


# Exercises
def show_exercises(exercises):
    """Load the exercises for the lesson"""
    if not exercises:
        st.info("No exercises for this lesson.")
        return

    for i, ex in enumerate(exercises):
        question = ex.get("exercise")
        if not question:
            continue  # skip malformed exercises
        user_input = st.text_input(question, key=f"ex_{i}")

        if user_input:
            correct_answer = ex.get("answer", "")
            feedback = ex.get("note", "")
            st.markdown(f"**Correct answer:** {correct_answer}")
            if feedback:
                st.info(f"Note: {feedback}")


# Main grammar mode
def run_grammar(level=None):
    """Main function for the grammar mode"""
    st.title("German Lessons")

    lessons = load_lessons()

    titles = list(lessons.keys())

    selected = st.selectbox("Choose lesson", titles)

    lesson = lessons[selected]

    st.header(lesson["title"])

    show_vocab(lesson["vocabulary"])

    show_examples(lesson["examples"])

    show_grammar(lesson["grammar_notes"])

    show_exercises(lesson["exercises"])