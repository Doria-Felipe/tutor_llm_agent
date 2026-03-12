import streamlit as st
from src.llm.client import get_llm
from src.agent.tools import build_german_tool

from src.audio.tts import speak
from src.audio.stt import transcribe
from streamlit_mic_recorder import mic_recorder


@st.cache_resource
def load_agent(model_name, level):
    llm = get_llm(model_name)
    return build_german_tool(llm, level)


def run_tutor(level="a1", show_sources=False, voice_mode=False):

    # st.title("🇩🇪 German AI Tutor")

    # ----------------------------
    # Session state
    # ----------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ----------------------------
    # Load agent once
    # ----------------------------

    agent = load_agent(st.session_state.model_name, level)

    # ----------------------------
    # Display chat history
    # ----------------------------

    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.markdown(message)

            if role == "assistant":
                audio_path = speak(message)
                st.audio(audio_path)

    # ----------------------------
    # Voice mode (optional)
    # ----------------------------

    if voice_mode:

        st.divider()
        st.subheader("🎤 Speak to the tutor")

        audio = mic_recorder(
            start_prompt="Start recording",
            stop_prompt="Stop recording",
            key="voice_input"
        )

        if audio:

            with st.spinner("Transcribing speech..."):
                user_query = transcribe(audio["bytes"])

            # show transcription
            with st.chat_message("user"):
                st.markdown(user_query)

            st.session_state.chat_history.append(("user", user_query))

            with st.spinner("Tutor thinking..."):
                answer = agent._run(user_query)

            with st.chat_message("assistant"):
                st.markdown(answer)

                audio_path = speak(answer)
                st.audio(audio_path)

            st.session_state.chat_history.append(("assistant", answer))

            # st.rerun()
            # Clear the mic so it doesn’t trigger rerun again
            st.session_state["voice_input"] = None

    # ----------------------------
    # Text input
    # ----------------------------

    user_query = st.chat_input("Ask something about German...")

    if user_query:

        with st.chat_message("user"):
            st.markdown(user_query)

        st.session_state.chat_history.append(("user", user_query))

        with st.spinner("Thinking..."):
            answer = agent._run(user_query)

        with st.chat_message("assistant"):
            st.markdown(answer)

            audio_path = speak(answer)
            st.audio(audio_path)

        st.session_state.chat_history.append(("assistant", answer))