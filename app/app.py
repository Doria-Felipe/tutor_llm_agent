import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sidebar import render_sidebar
from session import init_session
from styles import apply_styles

from modes.tutor_mode import run_tutor
from modes.vocab_mode import run_vocab
from modes.grammar_mode import run_grammar
from modes.quiz_mode import run_quiz


st.set_page_config(
    page_title="AVAA German",
    page_icon="AVAA",
    layout="centered",
    initial_sidebar_state="expanded"
)

apply_styles()

init_session()

# HERO HEADER
st.markdown(
"""
# AVAA German AI Tutor

Learn German using **real transcripts, AI explanations, and spaced repetition**.

""")

mode, level, show_sources, voice_mode = render_sidebar()

st.divider()

# ROUTER

if mode == "tutor":
    run_tutor(level, show_sources, voice_mode)

elif mode == "vocab":
    run_vocab(level)

elif mode == "grammar":
    run_grammar()

elif mode == "quiz":
    run_quiz(level)