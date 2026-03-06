import sys
from pathlib import Path

# Add parent folder of 'src/' to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import streamlit as st
import time

from src.agent.german_agent import german_agent
from src.rag.retriever import return_context
from src.llm.ollama_client import get_llm
from data.topic_lookup import get_topics, get_video_ids_by_topic
from src.rag.retriever import return_context_by_video_ids


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
# Cached vocab loader
# ------------------------

@st.cache_data
def load_vocab():
    with open("data/topics_vocab_clean.json", encoding="utf8") as f:
        return json.load(f)


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

    if mode == "vocab":
        topics = get_topics()
        selected_topic = st.selectbox("Choose topic", topics)
    else:
        selected_topic = None

    level = st.selectbox(
        "CEFR Level",
        ["a1", "a2", "b1", "b2", "c1", "c2"]
    )

    show_sources = st.checkbox("Show sources", value=True)

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()


# =====================================================
# VOCAB MODE (STATIC DATASET)
# =====================================================

if mode == "vocab" and selected_topic:

    st.header(f"📚 Vocabulary: {selected_topic}")

    vocab_data = load_vocab()

    topic_words = vocab_data.get(selected_topic, [])

    # Difficulty filtering
    topic_words = [
        w for w in topic_words
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

                    current = st.session_state.flashcard_state.get(key, False)
                    st.session_state.flashcard_state[key] = not current

                if st.session_state.flashcard_state.get(key, False):

                    st.markdown(f"**Meaning:** {w['meaning']}")
                    st.markdown(f"*Example:* {w['example']}")

    st.stop()


# =====================================================
# CHAT MODES
# =====================================================

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

            llm = get_llm(st.session_state.model_name)

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