import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.header("Settings")

        model_name = st.selectbox(
            "Model",
            ["llama3.1", "mistral", "qwen2.5:3b"]
        )

        mode = st.selectbox(
            "Mode",
            ["tutor", "vocab", "grammar", "quiz"]
        )

        level = st.selectbox(
            "CEFR Level",
            ["a1","a2","b1","b2","c1","c2"]
        )

        show_sources = st.checkbox("Show sources", value=True)

        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

    st.session_state.model_name = model_name

    return mode, level, show_sources