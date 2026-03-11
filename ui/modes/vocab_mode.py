import streamlit as st
import json
import random

VOCAB_PATH = "data/topics_vocab_clean.json"

# Load vocab
def load_vocab(level=None):
    """Loads the prepared JSON file

    Args:
        level (str, optional): The level the tutor is in. Defaults to None.

    Returns:
        lst: Returns a list of words
    """
    with open(VOCAB_PATH, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    words = []
    for entries in vocab.values():
        words.extend(entries)

    if level:
        words = [w for w in words if w.get("level") == level]

    random.shuffle(words)
    return words


# Session init
def init_session(level=None):
    """Initiating the session with a word.

    Args:
        level (str, optional): The level the tutor is in. Defaults to None.
    """
    if "words" not in st.session_state:
        st.session_state.words = load_vocab(level)

    if "vocab_index" not in st.session_state:
        st.session_state.vocab_index = 0

    if "show_translation" not in st.session_state:
        st.session_state.show_translation = False


# Next card
def next_card():
    """Get the next word from the list
    """
    st.session_state.vocab_index = (
        st.session_state.vocab_index + 1
    ) % len(st.session_state.words)

    st.session_state.show_translation = False


# -----------------------------
# Spaced repetition
# -----------------------------
def mark_easy():
    """Give points if user finds it easier
    """
    idx = st.session_state.vocab_index
    word = st.session_state.words.pop(idx)

    st.session_state.words.append(word)

    next_card()
    st.rerun()


def mark_medium():
    """Give points if user finds it medium
    """
    next_card()
    st.rerun()


def mark_hard():
    """Give points if user finds it hard
    """
    idx = st.session_state.vocab_index
    word = st.session_state.words.pop(idx)

    insert_idx = min(idx + 2, len(st.session_state.words))
    st.session_state.words.insert(insert_idx, word)

    next_card()
    st.rerun()


# UI Card
def show_card(entry):
    """The actual card with a word from the list"""
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
                color:white;">
                {entry['example']}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        if st.button("Reveal Translation"):

            st.session_state.show_translation = True
            st.rerun()


# Main vocab mode
def run_vocab(level=None):
    """The actual main for the vocabulary mode.
       It mostly orchestrate this mode.
    Args:
        level (str, optional): The level the tutor is in. Defaults to None.
    """
    st.title("Vocabulary Trainer")

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
        if st.button("Easy"):
            mark_easy()

    with col2:
        if st.button("Medium"):
            mark_medium()

    with col3:
        if st.button("Hard"):
            mark_hard()

    st.write("")
    st.progress((idx + 1) / len(st.session_state.words))