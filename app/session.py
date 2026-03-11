import streamlit as st


def init_session():
    defaults = {
        "messages": [],
        "vocab_topic": None,
        "vocab_subtopic": None,
        "vocab_index": 0,
        "show_translation": False,

        # spaced repetition memory
        "srs_data": {}
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value