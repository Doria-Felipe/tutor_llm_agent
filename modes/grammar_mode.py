import streamlit as st
import json
import re


@st.cache_data
def load_lessons():
    with open("data/grammar_lessons_explained.json", encoding="utf8") as f:
        return json.load(f)


def clean_title(title):
    return re.sub(r"\|.*", "", title).strip()


def run_grammar():

    st.header("📚 German Lessons")

    lessons = load_lessons()

    if not lessons:
        st.info("No lessons found.")
        return

    title_map = {clean_title(k): k for k in lessons.keys()}

    lesson_titles = sorted(title_map.keys())

    selected = st.selectbox("Choose lesson", lesson_titles)

    lesson = lessons.get(title_map[selected], {})

    st.subheader(lesson["title"])

    # Grammar explanation
    if lesson.get("grammar_explanation"):

        st.markdown("### 📖 Grammar")
        st.info(lesson["grammar_explanation"])

    # Vocabulary
    if lesson.get("vocabulary"):

        st.markdown("### 📚 Vocabulary")

        col1, col2 = st.columns(2)

        for i, v in enumerate(lesson["vocabulary"]):

            with (col1 if i % 2 == 0 else col2):

                with st.container(border=True):

                    st.markdown(f"### 🇩🇪 {v['word']}")
                    st.markdown(f"**Meaning:** {v['translation']}")

                    if v.get("explanation"):
                        st.caption(v["explanation"])

    # Examples
    if lesson.get("examples"):

        st.markdown("### ✏️ Examples")

        for ex in lesson["examples"]:

            with st.container(border=True):

                st.markdown(f"**🇩🇪 {ex['german']}**")
                st.markdown(f"🇬🇧 {ex['english']}")

                if ex.get("explanation"):
                    st.caption(ex["explanation"])