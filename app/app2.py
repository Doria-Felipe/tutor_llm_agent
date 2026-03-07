import sys
from pathlib import Path
import json
import re
import time

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from src.agent.german_agent import german_agent
from src.rag.retriever import return_context
from src.rag.retriever import return_context_by_video_ids
from src.llm.ollama_client import get_llm
from src.agent.lesson_agent import lesson_agent
from data.topic_lookup import get_topics, get_video_ids_by_topic
from data.grammar_lookup import get_grammar_topics, get_examples_by_topic

# ------------------------
# Page Config
# ------------------------

st.set_page_config(
    page_title="German RAG Tutor 🇩🇪",
    page_icon="🇩🇪",
    layout="centered"
)

st.title("🇩🇪 German RAG Tutor")
st.caption("Chat with authentic German learning transcripts")


# ------------------------
# Cached
# ------------------------

@st.cache_data
def load_vocab():
    with open("data/topics_vocab_clean.json", encoding="utf8") as f:
        return json.load(f)

@st.cache_data
def load_lessons():
    with open("data/grammar_lessons_explained.json", encoding="utf8") as f:
        return json.load(f)

@st.cache_resource
def load_llm(model):
    return get_llm(model)

# ------------------------
# Session State
# ------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_name" not in st.session_state:
    st.session_state.model_name = "llama3.1"

if "flashcard_state" not in st.session_state:
    st.session_state.flashcard_state = {}


# ------------------------
# Sidebar
# ------------------------

with st.sidebar:

    st.header("Settings")

    st.session_state.model_name = st.selectbox(
        "Model",
        ["llama3.1", "mistral", "qwen2.5:3b"]
    )

    mode = st.selectbox(
        "Mode",
        ["tutor", "vocab", "grammar", "quiz"]
    )

    level = st.selectbox(
        "CEFR Level",
        ["a1", "a2", "b1", "b2", "c1", "c2"]
    )

    show_sources = st.checkbox("Show sources", value=True)

    if "last_mode" not in st.session_state:
        st.session_state.last_mode = mode

    if mode != st.session_state.last_mode:
        st.session_state.messages = []
        st.session_state.last_mode = mode

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# =====================================================
# VOCAB MODE
# =====================================================

if mode == "vocab":

    topics = get_topics()
    selected_topic = st.selectbox("Choose topic", topics)

    if selected_topic:

        st.header(f"📚 Vocabulary: {selected_topic}")

        vocab_data = load_vocab()

        topic_words = [
            w for w in vocab_data.get(selected_topic, [])
            if w["level"].lower() == level.lower()
        ]

        if not topic_words:
            st.info("No vocabulary found for this level.")
            st.stop()

        col1, col2 = st.columns(2)

        for i, w in enumerate(topic_words):

            key = f"{selected_topic}_{i}"

            with (col1 if i % 2 == 0 else col2):

                with st.container(border=True):

                    st.markdown(f"### 🇩🇪 {w['word']}")

                    if st.button("Flip card", key=key):
                        st.session_state.flashcard_state[key] = not st.session_state.flashcard_state.get(key, False)

                    if st.session_state.flashcard_state.get(key, False):

                        st.markdown(f"**Meaning:** {w['meaning']}")
                        st.markdown(f"*Example:* {w['example']}")

    st.stop()


# =====================================================
# LESSON MODE
# =====================================================

def clean_title(title):
    return re.sub(r"\|.*", "", title).strip()

if mode == "grammar":

    st.header("📚 German Lessons")

    lessons = load_lessons()

    if not lessons:
        st.info("No lessons found.")
        st.stop()

    # lesson_titles = sorted(list(lessons.keys()))

    lesson_titles = sorted([clean_title(t) for t in lessons.keys()])
    
    selected_lesson = st.selectbox(
        "Choose lesson",
        lesson_titles
    )

    lesson = lessons[selected_lesson]

    st.subheader(lesson["title"])

    # ------------------------
    # Grammar Explanation
    # ------------------------

    if lesson.get("grammar_explanation"):

        st.markdown("### 📖 Grammar")

        st.info(lesson["grammar_explanation"])


    # ------------------------
    # Vocabulary
    # ------------------------

    if lesson.get("vocabulary"):

        st.markdown("### 📚 Vocabulary")

        col1, col2 = st.columns(2)

        for i, v in enumerate(lesson["vocabulary"]):

            with (col1 if i % 2 == 0 else col2):

                with st.container(border=True):

                    st.markdown(f"### 🇩🇪 {v['word']}")

                    st.markdown(
                        f"**Meaning:** {v['translation']}"
                    )

                    if v.get("explanation"):
                        st.caption(v["explanation"])


    # ------------------------
    # Examples
    # ------------------------

    if lesson.get("examples"):

        st.markdown("### ✏️ Examples")

        for ex in lesson["examples"]:

            with st.container(border=True):

                st.markdown(f"**🇩🇪 {ex['german']}**")

                st.markdown(f"🇬🇧 {ex['english']}")

                if ex.get("explanation"):
                    st.caption(ex["explanation"])


    st.stop()

# =====================================================
# CHAT MODES
# =====================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =====================================================
# CHAT MODES ONLY
# =====================================================

if mode in ["tutor", "quiz"]:

    # ------------------------
    # Display Chat History
    # ------------------------

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


    # ------------------------
    # Chat Input
    # ------------------------

    if prompt := st.chat_input("Ask something about German..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                start_time = time.time()

                # llm = get_llm(st.session_state.model_name)
                llm = load_llm(st.session_state.model_name)

                context = return_context(prompt, k=2)

                response = german_agent(
                    llm=llm,
                    user_query=prompt,
                    ctx=context,
                    mode=mode,
                    level=level
                )

                latency = round(time.time() - start_time, 2)

            st.markdown(response)
            st.caption(f"⏱ {latency}s")

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )