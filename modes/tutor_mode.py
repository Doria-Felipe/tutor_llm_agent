import streamlit as st
import time

from src.agent.german_agent import german_agent
from src.rag.hybrid_retriever import return_context
# from llm.client import get_llm
from src.llm.client import get_llm

@st.cache_resource
def load_llm(model):
    return get_llm(model)


def run_tutor(level, show_sources):

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask something about German..."):

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                start = time.time()

                # llm = get_llm(st.session_state.model_name)
                llm = load_llm(st.session_state.model_name)

                # context = return_context(prompt,k=2)
                if len(prompt.split()) < 4:
                    context = ""
                else:
                    context = return_context(prompt, k=2)

                response = german_agent(
                    llm=llm,
                    user_query=prompt,
                    ctx=context,
                    mode="tutor",
                    level=level
                )

                latency = round(time.time()-start,2)

            st.markdown(response)
            st.caption(f"⏱ {latency}s")

        st.session_state.messages.append(
            {"role":"assistant","content":response}
        )