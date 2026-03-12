import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.title("⚙️ Settings")

        model_name = st.selectbox(
            "Model",
            ["qwen2.5:3b","llama3.1","mistral"]
        )

        mode = st.radio(
            "Mode",
            ["tutor","vocab","grammar","quiz"]
        )

        level = st.selectbox(
            "German Level",
            ["a1","a2","b1","b2","c1","c2"]
        )

        voice_mode = st.checkbox("Voice Mode", value=False)

        show_sources = st.checkbox("Show sources", value=True)

        st.divider()

        if st.button("🧹 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    st.session_state.model_name = model_name

    return mode, level, show_sources, voice_mode