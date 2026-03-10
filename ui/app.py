import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from ui.sidebar import render_sidebar
from ui.session import init_session

from modes.tutor_mode import run_tutor
from modes.vocab_mode import run_vocab
from modes.grammar_mode import run_grammar
from modes.quiz_mode import run_quiz

# -----------------------------
# Session state for cover
# -----------------------------
if "entered" not in st.session_state:
    st.session_state.entered = False

# -----------------------------
# Session state for cover
# -----------------------------
if "entered" not in st.session_state:
    st.session_state.entered = False

# -----------------------------
# Cover page
# -----------------------------
if not st.session_state.entered:
    st.title("🇩🇪 German RAG Tutor")
    st.subheader("Learn German with AI-powered lessons and quizzes!")
    
    # Optional cover image (replace path with your own image)
    try:
        st.image("assets/cover_image.png")
    except:
        pass
    
    st.markdown(
        """
        Welcome to your interactive German tutor!  

        Choose a mode to get started:
        - Vocabulary practice
        - Grammar lessons
        - Interactive quizzes
        """
    )

    if st.button("Enter Tutor"):
        st.session_state.entered = True

    st.stop()  # Stop here until user clicks "Enter Tutor"
    
st.set_page_config(
    page_title="German RAG Tutor 🇩🇪",
    page_icon="🇩🇪",
    layout="centered"
)

st.title("🇩🇪 German RAG Tutor")
st.caption("Chat with authentic German learning transcripts")

init_session()

mode, level, show_sources = render_sidebar()

# ROUTER

if mode == "tutor":
    run_tutor(level, show_sources)

elif mode == "vocab":
    run_vocab(level)

elif mode == "grammar":
    run_grammar()

elif mode == "quiz":
    run_quiz(level)