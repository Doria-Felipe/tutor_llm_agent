import os
from dotenv import load_dotenv, find_dotenv
from sentence_transformers import SentenceTransformer

_ = load_dotenv(find_dotenv())

HF_TOKEN  = os.getenv("HF_TOKEN")

_model = None

def get_model():
    global _model
    if _model is None:
        # _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", cache_folder="./hf_cache", token=HF_TOKEN)
    return _model