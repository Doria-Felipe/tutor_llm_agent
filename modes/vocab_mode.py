# import streamlit as st
# import json
# from data.topic_lookup import get_topics


# @st.cache_data
# def load_vocab():
#     with open("data/topics_vocab_clean.json",encoding="utf8") as f:
#         return json.load(f)


# def run_vocab(level):

#     topics = get_topics()

#     topic = st.selectbox("Choose topic",topics)

#     vocab = load_vocab()

#     words = [
#         w for w in vocab.get(topic,[])
#         if w["level"].lower()==level.lower()
#     ]

#     col1,col2 = st.columns(2)

#     for i,w in enumerate(words):

#         with (col1 if i%2==0 else col2):

#             with st.container(border=True):

#                 st.markdown(f"### 🇩🇪 {w['word']}")
#                 st.markdown(f"**Meaning:** {w['meaning']}")
#                 st.markdown(f"*Example:* {w['example']}")

import streamlit as st
import json
from scripts.topic_lookup import get_topics
from pathlib import Path

VOCAB_PATH = Path("data/topics_vocab_clean.json")

# -------------------------
# Load vocab
# -------------------------
@st.cache_data
def load_vocab():
    with open(VOCAB_PATH, encoding="utf8") as f:
        return json.load(f)

# -------------------------
# Run vocab mode
# -------------------------
def run_vocab(level: str):

    st.header("📚 Vocabulary Mode")

    vocab = load_vocab()
    topics = get_topics()

    # -------------------------
    # Main topic selectbox
    # -------------------------
    main_topics = sorted({t.split(" → ")[0] for t in topics})
    selected_main = st.selectbox("Select Main Topic", main_topics)

    # Subtopic filter
    subtopics = sorted([t.split(" → ")[1] for t in topics if t.startswith(selected_main)])
    selected_sub = st.selectbox("Select Subtopic", subtopics)

    selected_topic = f"{selected_main} → {selected_sub}"

    words = [
        w for w in vocab.get(selected_topic, [])
        if w["level"].lower() == level.lower()
    ]

    if not words:
        st.info("No words found for this topic and level.")
        st.stop()

    # -------------------------
    # Display flip cards
    # -------------------------
    col1, col2 = st.columns(2)
    for i, w in enumerate(words):
        col = col1 if i % 2 == 0 else col2
        key = f"{selected_topic}_{i}"
        show_example = st.session_state.get("flashcard_state", {}).get(key, False)

        with col:
            st.markdown(f"### 🇩🇪 {w['word']}")

            if st.button("Flip card", key=key):
                if "flashcard_state" not in st.session_state:
                    st.session_state.flashcard_state = {}
                st.session_state.flashcard_state[key] = not show_example
                show_example = not show_example

            if show_example:
                st.markdown(f"**Meaning:** {w['meaning']}")
                st.markdown(f"*Example:* {w['example']}")