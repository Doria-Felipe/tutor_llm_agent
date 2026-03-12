import streamlit as st

def apply_styles():

    st.markdown(
        """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Poppins:wght@500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">

<style>

/* base font */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* titles */

h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
    letter-spacing: -0.02em;
}

/* german examples */

.example {
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
}

/* cards */

.card {
    background: #1e1e1e;
    padding: 28px;
    border-radius: 16px;
    border: 1px solid #2d2d2d;
}

/* tutor bubbles */

.user-msg {
    background: #2a2a2a;
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.assistant-msg {
    background: #1b263b;
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 16px;
}

/* flashcards */

.flashcard {
    background: linear-gradient(145deg,#1e1e1e,#121212);
    border-radius: 20px;
    padding: 60px;
    text-align:center;
    font-size:44px;
    font-weight:600;
    border:1px solid #333;
}

/* translation */

.translation {
    text-align:center;
    font-size:28px;
    margin-top:20px;
}

</style>
""",
        unsafe_allow_html=True
    )