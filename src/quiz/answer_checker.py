import numpy as np
from src.embeddings.model import get_model
import streamlit as st

@st.cache_resource
def load_model():
    return get_model()

model = load_model()


def check_answer(user_answer, correct_answer):

    emb = model.encode(
        [user_answer, correct_answer],
        normalize_embeddings=True
    )

    similarity = float(np.dot(emb[0], emb[1]))

    if similarity > 0.75:
        return True, similarity

    return False, similarity