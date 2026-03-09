import streamlit as st

def init_session():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "model_name" not in st.session_state:
        st.session_state.model_name = "llama3.1"

    if "flashcard_state" not in st.session_state:
        st.session_state.flashcard_state = {}