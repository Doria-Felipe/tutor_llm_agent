import streamlit as st
from src.llm.client import get_llm
from src.agent.tools import build_german_tool


@st.cache_resource
def load_agent(model_name, level):
    llm = get_llm(model_name)
    return build_german_tool(llm, level)


def run_tutor(level="a1", show_sources=False):

    st.header("Tutor")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # -----------------------------
    # Input form (prevents rerun issues)
    # -----------------------------
    with st.form("tutor_form", clear_on_submit=True):

        user_query = st.text_input(
            "Ask a question about German",
            placeholder="Example: How do I say 'I am learning German'?"
        )

        submitted = st.form_submit_button("Ask")

    # -----------------------------
    # Run agent
    # -----------------------------
    if submitted and user_query:

        agent = load_agent(st.session_state.model_name, level)

        with st.spinner("Thinking..."):
            answer = agent._run(user_query)

        st.session_state.chat_history.append((user_query, answer))

    # -----------------------------
    # Chat history
    # -----------------------------
    # for q, a in reversed(st.session_state.chat_history):

    #     st.markdown(f"**Q:** {q}")
    #     st.markdown(f"**A:** {a}")
    #     st.markdown("---")
    for q, a in reversed(st.session_state.chat_history):

        st.markdown(f'<div class="user-msg"> Q: {q}</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="assistant-msg"> A: {a}</div>',
            unsafe_allow_html=True
                    )