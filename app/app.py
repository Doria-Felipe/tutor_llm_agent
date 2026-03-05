import sys
from pathlib import Path

# Add parent folder of 'src/' to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import time

from src.agent.german_agent import german_agent
from src.rag.retriever import return_context
from src.llm.ollama_client import get_llm
from data.topic_lookup import get_topics, get_video_ids_by_topic
from src.rag.retriever import return_context_by_video_ids


# ------------------------
# Page Config
# ------------------------

st.set_page_config(
    page_title="German RAG Tutor 🇩🇪",
    page_icon="🇩🇪",
    layout="centered"
)

st.title("🇩🇪 German RAG Tutor")
st.caption("Chat with authentic German learning transcripts")


# ------------------------
# Session State
# ------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_name" not in st.session_state:
    st.session_state.model_name = "llama3.1"


# ------------------------
# Sidebar
# ------------------------

with st.sidebar:
    st.header("Settings")

    st.session_state.model_name = st.selectbox(
        "Model",
        ["llama3.1", "mistral", "qwen2.5:3b"]
    )

    mode = st.selectbox(
        "Mode",
        ["tutor", "vocab", "grammar", "quiz"]
    )

    if mode == "vocab":
        topics = get_topics()
        selected_topic = st.selectbox("Choose topic", topics)
    else:
        selected_topic = None

    level = st.selectbox(
        "CEFR Level",
        ["a1", "a2", "b1", "b2", "c1", "c2"]
    )

    show_sources = st.checkbox("Show sources", value=True)

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()


# ------------------------
# Display Chat History
# ------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ------------------------
# Chat Input
# ------------------------
if prompt := st.chat_input("Ask something about German..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()
            llm = get_llm(st.session_state.model_name)

            # ------------------------
            # Context retrieval
            # ------------------------
            if mode == "vocab" and selected_topic:
                # vocab mode → context is already a string
                video_ids = get_video_ids_by_topic(selected_topic)
                context = return_context_by_video_ids(
                    query=selected_topic,
                    video_ids=video_ids,
                    k=3
                )
                prompt_to_llm = f"Teach vocabulary about {selected_topic}"
                docs_for_sources = None  # vocab mode does not have docs
            else:
                # other modes → return_context returns list of dicts
                docs_for_sources = None
                context = return_context(prompt, k=2)
                prompt_to_llm = prompt

            # ------------------------
            # Generate response
            # ------------------------
            response = german_agent(
                llm=llm,
                user_query=prompt_to_llm,
                ctx=context,
                mode=mode,
                level=level
            )

            latency = round(time.time() - start_time, 2)

        st.markdown(response)
        st.caption(f"⏱ {latency}s")

        # ------------------------
        # Optional sources
        # ------------------------
        if show_sources and docs_for_sources:
            with st.expander("📚 Sources"):
                for doc in docs_for_sources:
                    title = doc["metadata"].get("title", "Unknown")
                    start = doc["metadata"].get("start", 0)
                    end = doc["metadata"].get("end", 0)
                    st.markdown(f"- **{title}** ({int(start)}s – {int(end)}s)")

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )