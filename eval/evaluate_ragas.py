# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).resolve().parents[1]))

# import re
# import pandas as pd
# from datasets import Dataset
# from tqdm import tqdm

# from langchain_huggingface import HuggingFaceEmbeddings
# from ragas import evaluate
# from ragas.run_config import RunConfig

# from ragas.metrics._answer_relevance import AnswerRelevancy
# from ragas.metrics._faithfulness import Faithfulness
# from ragas.metrics._context_precision import ContextPrecision
# from ragas.metrics._context_recall import ContextRecall

# from langchain_ollama import ChatOllama
# from ragas.llms import LangchainLLMWrapper
# from src.llm.client import get_llm

# from sklearn.metrics.pairwise import cosine_similarity
# from src.rag.hybrid_retriever import hybrid_search, format_context

# # -----------------------------
# # Helper functions
# # -----------------------------
# def extract_answer(text: str) -> str:
#     """
#     Extract the real German answer from verbose tutor outputs.
#     """
#     if not isinstance(text, str) or text.strip() == "":
#         return ""

#     text = text.strip()

#     # patterns commonly produced by your tutor
#     patterns = [
#         r"The correct answer is:\s*(.*?)(?:\.|\n)",
#         r"The answer is:\s*(.*?)(?:\.|\n)",
#         r"The correct completion of the sentence is:\s*(.*?)(?:\.|\n)",
#         r"The correct sentence is:\s*(.*?)(?:\.|\n)",
#     ]

#     for pattern in patterns:
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             return match.group(1).strip().replace('"', "")

#     # fallback: first line
#     first_line = text.split("\n")[0]
#     first_line = re.sub(r"The correct answer is:\s*", "", first_line, flags=re.I)
#     first_line = re.sub(r"The answer is:\s*", "", first_line, flags=re.I)
#     return first_line.strip()


# def split_context(text: str):
#     """
#     Split a context string into individual sentences.
#     """
#     if not isinstance(text, str) or text.strip() == "":
#         return []
#     sentences = re.split(r'(?<=[.!?])\s+', text.strip())
#     return [s.strip() for s in sentences if s.strip()]


# # -----------------------------
# # SETTINGS
# # -----------------------------
# EVAL_PERCENTAGE = 0.08       # fraction of questions to evaluate
# RANDOM_SEED = 42
# TOP_K = 5                    # number of top contexts to select

# INPUT_PATH = "data/generated_agent_answers.csv"

# embedding_model = HuggingFaceEmbeddings(
#     model_name="intfloat/multilingual-e5-base"
# )

# judge_llm = LangchainLLMWrapper(get_llm())

# metrics = [
#     ContextPrecision(llm=judge_llm),
#     ContextRecall(llm=judge_llm),
#     AnswerRelevancy(llm=judge_llm),
#     Faithfulness(llm=judge_llm)
# ]

# # -----------------------------
# # LOAD DATA
# # -----------------------------
# df = pd.read_csv(INPUT_PATH)

# # Extract real answer
# df["answer_clean"] = df["answer"].apply(extract_answer)

# # Select sample for evaluation
# df_sample = df.sample(frac=EVAL_PERCENTAGE, random_state=RANDOM_SEED)
# print(f"Evaluating {len(df_sample)} / {len(df)} questions")

# # Retrieve top-k contexts using your retriever
# ragas_dataset_list = []

# for _, row in tqdm(df_sample.iterrows(), total=len(df_sample)):
#     question = row["question"]
#     answer = row["answer_clean"]        # Use cleaned answer
#     ground_truth = row["ground_truth"]

#     results = hybrid_search(question, k=TOP_K)
#     top_contexts = [r["doc"] for r in results]

#     ragas_dataset_list.append({
#         "question": question,
#         "contexts": top_contexts,
#         "answer": answer,
#         "ground_truth": ground_truth
#     })

# dataset = Dataset.from_list(ragas_dataset_list)

# # -----------------------------
# # RUN RAGAS EVALUATION
# # -----------------------------
# result = evaluate(
#     dataset,
#     metrics=metrics,
#     llm=judge_llm,
#     embeddings=embedding_model,
#     run_config=RunConfig(
#         timeout=1800,
#         max_workers=1
#     )
# )

# # -----------------------------
# # PRINT RESULTS
# # -----------------------------
# print("\nEvaluation Results\n")
# print(result)

# # -----------------------------
# # SAVE RESULTS
# # -----------------------------
# results_df = pd.DataFrame([result])
# results_df.to_csv("data/ragas_results.csv", index=False)
# df.to_csv("data/evaluated_subset.csv", index=False)

# print("\nSaved results to data/ragas_results.csv and data/evaluated_subset.csv")


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import re
import pandas as pd
from datasets import Dataset
from tqdm import tqdm

from langchain_huggingface import HuggingFaceEmbeddings
from ragas import evaluate
from ragas.run_config import RunConfig

from ragas.metrics._answer_relevance import AnswerRelevancy
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._context_precision import ContextPrecision
from ragas.metrics._context_recall import ContextRecall

from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper
from src.llm.client import get_llm

from src.rag.hybrid_retriever import hybrid_search


# -----------------------------
# Helper functions
# -----------------------------
def extract_answer(text: str) -> str:
    """
    Extract the real German answer from verbose tutor outputs.
    """
    if not isinstance(text, str) or text.strip() == "":
        return ""

    text = text.strip()

    patterns = [
        r"The correct answer is:\s*(.*?)(?:\.|\n)",
        r"The answer is:\s*(.*?)(?:\.|\n)",
        r"The correct completion of the sentence is:\s*(.*?)(?:\.|\n)",
        r"The correct sentence is:\s*(.*?)(?:\.|\n)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))

    # fallback: first line
    first_line = text.split("\n")[0]
    first_line = re.sub(r"The correct answer is:\s*", "", first_line, flags=re.I)
    first_line = re.sub(r"The answer is:\s*", "", first_line, flags=re.I)

    return clean_text(first_line)


def clean_text(text: str) -> str:
    """
    Normalize text so RAGAS parsers don't fail.
    """
    text = text.replace('"', '')
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_context(text: str):
    """
    Split context block into sentences for RAGAS retrieved_contexts.
    """
    if not isinstance(text, str) or text.strip() == "":
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [clean_text(s) for s in sentences if s.strip()]

    # limit context size to avoid parser overload
    return sentences[:20]


# -----------------------------
# SETTINGS
# -----------------------------
EVAL_PERCENTAGE = 0.08
RANDOM_SEED = 42
TOP_K = 5

INPUT_PATH = "data/generated_agent_answers.csv"

embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)

judge_llm = LangchainLLMWrapper(get_llm())

metrics = [
    ContextPrecision(llm=judge_llm),
    ContextRecall(llm=judge_llm),
    AnswerRelevancy(llm=judge_llm),
    Faithfulness(llm=judge_llm)
]


# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(INPUT_PATH)

df["answer_clean"] = df["answer"].apply(extract_answer)
df["ground_truth"] = df["ground_truth"].apply(clean_text)

df_sample = df.sample(frac=EVAL_PERCENTAGE, random_state=RANDOM_SEED)

print(f"Evaluating {len(df_sample)} / {len(df)} questions")


# -----------------------------
# BUILD RAGAS DATASET
# -----------------------------
ragas_dataset_list = []

for _, row in tqdm(df_sample.iterrows(), total=len(df_sample)):

    question = clean_text(row["question"])
    answer = row["answer_clean"]
    ground_truth = row["ground_truth"]

    results = hybrid_search(question, k=TOP_K)

    contexts = [r["doc"] for r in results]
    contexts = split_context(" ".join(contexts))

    ragas_dataset_list.append({
        "question": question,
        "retrieved_contexts": contexts,
        "answer": answer,
        "ground_truth": ground_truth
    })

dataset = Dataset.from_list(ragas_dataset_list)


# -----------------------------
# RUN RAGAS
# -----------------------------
result = evaluate(
    dataset,
    metrics=metrics,
    llm=judge_llm,
    embeddings=embedding_model,
    run_config=RunConfig(
        timeout=1800,
        max_workers=1
    )
)


# -----------------------------
# PRINT RESULTS
# -----------------------------
print("\nEvaluation Results\n")
print(result)


# -----------------------------
# SAVE RESULTS
# -----------------------------
results_df = pd.DataFrame([result])
results_df.to_csv("data/ragas_results_20.csv", index=False)
df.to_csv("data/evaluated_subset_20.csv", index=False)

print("\nSaved results to data/ragas_results.csv and data/evaluated_subset.csv")