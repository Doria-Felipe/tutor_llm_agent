# import streamlit as st
# import json
# import re


# @st.cache_data
# def load_lessons():
#     with open("data/grammar_lessons_explained.json", encoding="utf8") as f:
#         return json.load(f)


# def clean_title(title):
#     return re.sub(r"\|.*", "", title).strip()


# def run_grammar():

#     st.header("📚 German Lessons")

#     lessons = load_lessons()

#     if not lessons:
#         st.info("No lessons found.")
#         return

#     title_map = {clean_title(k): k for k in lessons.keys()}

#     lesson_titles = sorted(title_map.keys())

#     selected = st.selectbox("Choose lesson", lesson_titles)

#     lesson = lessons.get(title_map[selected], {})

#     st.subheader(lesson["title"])

#     # Grammar explanation
#     if lesson.get("grammar_explanation"):

#         st.markdown("### 📖 Grammar")
#         st.info(lesson["grammar_explanation"])

#     # Vocabulary
#     if lesson.get("vocabulary"):

#         st.markdown("### 📚 Vocabulary")

#         col1, col2 = st.columns(2)

#         for i, v in enumerate(lesson["vocabulary"]):

#             with (col1 if i % 2 == 0 else col2):

#                 with st.container(border=True):

#                     st.markdown(f"### 🇩🇪 {v['word']}")
#                     st.markdown(f"**Meaning:** {v['translation']}")

#                     if v.get("explanation"):
#                         st.caption(v["explanation"])

#     # Examples
#     if lesson.get("examples"):

#         st.markdown("### ✏️ Examples")

#         for ex in lesson["examples"]:

#             with st.container(border=True):

#                 st.markdown(f"**🇩🇪 {ex['german']}**")
#                 st.markdown(f"🇬🇧 {ex['english']}")

#                 if ex.get("explanation"):
#                     st.caption(ex["explanation"])

import streamlit as st
import json

LESSON_PATH = "data/grammar_lessons_explained.json"


# -----------------------------
# Load lessons
# -----------------------------
def load_lessons():

    with open(LESSON_PATH, encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Vocabulary block
# -----------------------------
def show_vocab(vocab):

    st.subheader("📚 Vocabulary")

    for v in vocab:

        with st.expander(f"{v['word']} — {v['translation']}"):

            if "note" in v:
                st.write(v["note"])


# -----------------------------
# Examples
# -----------------------------
def show_examples(examples):

    st.subheader("✏️ Examples")

    for ex in examples:

        st.markdown(f"🇩🇪 **{ex['german']}**")
        st.markdown(f"🇬🇧 {ex['english']}")

        if "note" in ex:
            st.caption(ex["note"])

        st.write("")


# -----------------------------
# Grammar Notes
# -----------------------------
def show_grammar(notes):

    if not notes:
        return

    st.subheader("📖 Grammar Notes")

    for n in notes:
        st.markdown(f"- {n}")


# -----------------------------
# Exercises
# -----------------------------
def show_exercises(exercises):

    if not exercises:
        return

    st.subheader("📝 Exercises")

    for i, ex in enumerate(exercises):

        user = st.text_input(ex["exercise"], key=f"ex_{i}")

        if user:

            if user.lower() in ex["answer"].lower():
                st.success("Correct!")
            else:
                st.info(f"Example answer: {ex['answer']}")


# -----------------------------
# Main grammar mode
# -----------------------------
def run_grammar(level=None):

    st.title("📚 German Lessons")

    lessons = load_lessons()

    titles = list(lessons.keys())

    selected = st.selectbox("Choose lesson", titles)

    lesson = lessons[selected]

    st.header(lesson["title"])

    show_vocab(lesson["vocabulary"])

    show_examples(lesson["examples"])

    show_grammar(lesson["grammar_notes"])

    show_exercises(lesson["exercises"])