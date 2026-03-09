import streamlit as st
import json
from data.topic_lookup import get_topics


@st.cache_data
def load_vocab():
    with open("data/topics_vocab_clean.json",encoding="utf8") as f:
        return json.load(f)


def run_vocab(level):

    topics = get_topics()

    topic = st.selectbox("Choose topic",topics)

    vocab = load_vocab()

    words = [
        w for w in vocab.get(topic,[])
        if w["level"].lower()==level.lower()
    ]

    col1,col2 = st.columns(2)

    for i,w in enumerate(words):

        with (col1 if i%2==0 else col2):

            with st.container(border=True):

                st.markdown(f"### 🇩🇪 {w['word']}")
                st.markdown(f"**Meaning:** {w['meaning']}")
                st.markdown(f"*Example:* {w['example']}")