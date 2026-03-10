# import streamlit as st
# import json
# import random

# VOCAB_PATH = "data/topics_vocab_clean.json"

# # -----------------------------
# # Load vocab
# # -----------------------------
# def load_vocab(level=None):
#     with open(VOCAB_PATH, "r", encoding="utf-8") as f:
#         vocab = json.load(f)
#     words = []
#     for entries in vocab.values():
#         words.extend(entries)
#     if level:
#         words = [w for w in words if w.get("level")==level]
#     random.shuffle(words)
#     return words

# # -----------------------------
# # Session initialization
# # -----------------------------
# def init_session(level=None):
#     if "words" not in st.session_state:
#         st.session_state.words = load_vocab(level)
#     if "vocab_index" not in st.session_state:
#         st.session_state.vocab_index = 0
#     if "show_translation" not in st.session_state:
#         st.session_state.show_translation = False

# # -----------------------------
# # Display card
# # -----------------------------
# def show_card(word_entry):
#     st.markdown(f"🟦 **{word_entry['word']}**")
#     if st.session_state.show_translation:
#         st.markdown(f"**Meaning:** {word_entry['meaning']}")
#         if "example" in word_entry:
#             st.markdown(f"**Example:** {word_entry['example']}")
#     else:
#         if st.button("Show translation", key="show_trans"):
#             st.session_state.show_translation = True
#             st.rerun()

# # -----------------------------
# # Spaced repetition actions
# # -----------------------------
# def mark_easy():
#     idx = st.session_state.vocab_index
#     word = st.session_state.words.pop(idx)
#     st.session_state.words.append(word)
#     next_card()
#     st.rerun()

# def mark_medium():
#     st.session_state.vocab_index = (st.session_state.vocab_index + 1) % len(st.session_state.words)
#     st.session_state.show_translation = False
#     st.rerun()

# def mark_hard():
#     idx = st.session_state.vocab_index
#     word = st.session_state.words.pop(idx)
#     insert_idx = min(idx + 2, len(st.session_state.words))
#     st.session_state.words.insert(insert_idx, word)
#     st.session_state.vocab_index = (st.session_state.vocab_index + 1) % len(st.session_state.words)
#     st.session_state.show_translation = False
#     st.rerun()

# # -----------------------------
# # Next card
# # -----------------------------
# def next_card():
#     st.session_state.vocab_index = (st.session_state.vocab_index + 1) % len(st.session_state.words)
#     st.session_state.show_translation = False

# # -----------------------------
# # Run Vocab Mode
# # -----------------------------
# def run_vocab(level=None):
#     st.title("🇩🇪 German RAG Tutor - Vocab Mode")
#     init_session(level)

#     if not st.session_state.words:
#         st.warning("No words found.")
#         return

#     idx = st.session_state.vocab_index
#     word_entry = st.session_state.words[idx]

#     show_card(word_entry)

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         if st.button("Easy", key=f"easy_{idx}"):
#             mark_easy()
#     with col2:
#         if st.button("Medium", key=f"med_{idx}"):
#             mark_medium()
#     with col3:
#         if st.button("Hard", key=f"hard_{idx}"):
#             mark_hard()

#     st.markdown(f"Progress: {idx+1}/{len(st.session_state.words)}")

import streamlit as st
import json
import random

VOCAB_PATH = "data/topics_vocab_clean.json"

# -----------------------------
# Load vocab
# -----------------------------
def load_vocab(level=None):
    with open(VOCAB_PATH, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    words = []
    for entries in vocab.values():
        words.extend(entries)

    if level:
        words = [w for w in words if w.get("level") == level]

    random.shuffle(words)
    return words


# -----------------------------
# Session init
# -----------------------------
def init_session(level=None):

    if "words" not in st.session_state:
        st.session_state.words = load_vocab(level)

    if "vocab_index" not in st.session_state:
        st.session_state.vocab_index = 0

    if "show_translation" not in st.session_state:
        st.session_state.show_translation = False


# -----------------------------
# Next card
# -----------------------------
def next_card():

    st.session_state.vocab_index = (
        st.session_state.vocab_index + 1
    ) % len(st.session_state.words)

    st.session_state.show_translation = False


# -----------------------------
# Spaced repetition
# -----------------------------
def mark_easy():

    idx = st.session_state.vocab_index
    word = st.session_state.words.pop(idx)

    st.session_state.words.append(word)

    next_card()
    st.rerun()


def mark_medium():

    next_card()
    st.rerun()


def mark_hard():

    idx = st.session_state.vocab_index
    word = st.session_state.words.pop(idx)

    insert_idx = min(idx + 2, len(st.session_state.words))
    st.session_state.words.insert(insert_idx, word)

    next_card()
    st.rerun()


# -----------------------------
# UI Card
# -----------------------------
def show_card(entry):

    st.markdown(
        f"""
        <div style="
        padding:40px;
        border-radius:15px;
        text-align:center;
        background-color:#1e1e1e;
        font-size:40px;
        font-weight:600;">
        {entry['word']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.session_state.show_translation:

        st.markdown(
            f"""
            <div style="
            text-align:center;
            font-size:28px;">
            {entry['meaning']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "example" in entry:

            st.markdown(
                f"""
                <div style="
                text-align:center;
                font-size:18px;
                color:gray;">
                {entry['example']}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        if st.button("Reveal Translation"):

            st.session_state.show_translation = True
            st.rerun()


# -----------------------------
# Main vocab mode
# -----------------------------
def run_vocab(level=None):

    st.title("🧠 Vocabulary Trainer")

    init_session(level)

    if not st.session_state.words:
        st.warning("No vocabulary found.")
        return

    idx = st.session_state.vocab_index
    entry = st.session_state.words[idx]

    show_card(entry)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("😄 Easy"):
            mark_easy()

    with col2:
        if st.button("😐 Medium"):
            mark_medium()

    with col3:
        if st.button("😓 Hard"):
            mark_hard()

    st.write("")
    st.progress((idx + 1) / len(st.session_state.words))