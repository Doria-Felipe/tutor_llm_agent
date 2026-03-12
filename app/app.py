import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# from app.sidebar import render_sidebar
# from app.session import init_session
from sidebar import render_sidebar
from session import init_session

from modes.tutor_mode import run_tutor
from modes.vocab_mode import run_vocab
from modes.grammar_mode import run_grammar
from modes.quiz_mode import run_quiz

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