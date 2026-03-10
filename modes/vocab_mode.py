import streamlit as st
import json
import random

# -----------------------------
# Config
# -----------------------------
VOCAB_PATH = "data/topics_vocab_clean.json"

# -----------------------------
# Load vocab once and cache
# -----------------------------
@st.cache_data
def load_vocab(level=None):
    with open(VOCAB_PATH, "r", encoding="utf-8") as f:
        vocab = json.load(f)
    # Flatten all words
    words = []
    for entries in vocab.values():
        words.extend(entries)
    if level:
        words = [w for w in words if w.get("level") == level]
    return words

# -----------------------------
# Initialize session state
# -----------------------------
def init_session(level=None):
    if "words" not in st.session_state:
        words = load_vocab(level)
        st.session_state.words = words
        random.shuffle(st.session_state.words)
    if "vocab_index" not in st.session_state:
        st.session_state.vocab_index = 0
    if "show_translation" not in st.session_state:
        st.session_state.show_translation = False

# -----------------------------
# Handlers
# -----------------------------
def show_translation():
    st.session_state.show_translation = True

def next_card():
    st.session_state.vocab_index = (st.session_state.vocab_index + 1) % len(st.session_state.words)
    st.session_state.show_translation = False

def mark_easy():
    idx = st.session_state.vocab_index
    word = st.session_state.words.pop(idx)
    st.session_state.words.append(word)
    next_card()

def mark_medium():
    next_card()

def mark_hard():
    idx = st.session_state.vocab_index
    word = st.session_state.words.pop(idx)
    insert_idx = min(idx + 2, len(st.session_state.words))
    st.session_state.words.insert(insert_idx, word)
    next_card()

# -----------------------------
# Show single flashcard
# -----------------------------
def show_card(word_entry):
    st.markdown(f"🟦 **{word_entry['word']}**")
    if st.session_state.show_translation:
        st.markdown(f"**Meaning:** {word_entry['meaning']}")
        if "example" in word_entry:
            st.markdown(f"**Example:** {word_entry['example']}")
    else:
        st.button(
            "Show translation",
            key=f"show_{st.session_state.vocab_index}",
            on_click=show_translation
        )

# -----------------------------
# Main Vocab Mode
# -----------------------------
def run_vocab(level=None):
    st.title("🇩🇪 German RAG Tutor - Vocab Mode")
    init_session(level)

    if not st.session_state.words:
        st.warning("No vocabulary words found.")
        return

    idx = st.session_state.vocab_index
    word_entry = st.session_state.words[idx]

    show_card(word_entry)

    # Buttons with callbacks
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.button("Easy", key=f"easy_{idx}", on_click=mark_easy)
    with col2:
        st.button("Medium", key=f"medium_{idx}", on_click=mark_medium)
    with col3:
        st.button("Hard", key=f"hard_{idx}", on_click=mark_hard)

    # Progress
    st.markdown(f"Progress: {idx+1} / {len(st.session_state.words)}")