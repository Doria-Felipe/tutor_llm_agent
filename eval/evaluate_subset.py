# import pandas as pd
# from datasets import Dataset

# # from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
# from ragas.embeddings import LangchainEmbeddingsWrapper

# from ragas import evaluate
# from ragas.run_config import RunConfig

# from ragas.metrics._answer_relevance import AnswerRelevancy
# from ragas.metrics._faithfulness import Faithfulness
# from ragas.metrics._context_precision import ContextPrecision
# from ragas.metrics._context_recall import ContextRecall


# from langchain_ollama import ChatOllama
# from ragas.llms import LangchainLLMWrapper


# # ---------- SETTINGS ----------

# EVAL_PERCENTAGE = 0.08
# RANDOM_SEED = 42
# metrics = [
#     # Faithfulness(),
#     AnswerRelevancy(),
#     ContextPrecision(),
#     # ContextRecall()
# ]

# embedding_model = LangchainEmbeddingsWrapper(
#     HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )
# )

# # ---------- LOAD GENERATED ANSWERS ----------

# df = pd.read_csv("eval/generated_answers.csv")

# df_sample = df.sample(
#     frac=EVAL_PERCENTAGE,
#     random_state=RANDOM_SEED
# )

# print(f"Evaluating {len(df_sample)} / {len(df)} questions")


# # ---------- CONVERT TO RAGAS DATASET ----------

# dataset = Dataset.from_list([
#     {
#         "question": row["question"],
#         "contexts": [row["context"]],
#         "answer": row["answer"],
#         "ground_truth": row["ground_truth"]
#     }
#     for _, row in df_sample.iterrows()
# ])


# # ---------- JUDGE MODEL (QWEN) ----------

# judge_llm = LangchainLLMWrapper(
#     ChatOllama(
#         model="qwen2.5:3b",
#         temperature=0,
#         format="json"
#     )
# )

# # ---------- RUN EVALUATION ----------

# # results = evaluate(
# #     dataset,
# #     metrics=[
# #         faithfulness,
# #         answer_relevancy,
# #         context_precision,
# #         context_recall
# #     ],
# #     llm=judge_llm
# # )
# # results = evaluate(
# #     dataset,
# #     metrics=[
# #         faithfulness(),
# #         answer_relevancy(),
# #         context_precision(),
# #         context_recall()
# #     ],
# #     llm=judge_llm
# # )
# # results = evaluate(
# #     dataset,
# #     metrics=metrics,
# #     llm=judge_llm
# # )

# # results = evaluate(
# #     dataset,
# #     metrics=metrics,
# #     llm=judge_llm,
# #     embeddings=embedding_model
# # )

# # result = evaluate(
# #     dataset,
# #     metrics=metrics,
# #     llm=judge_llm,
# #     embeddings=embedding_model,
# #     run_config=RunConfig(
# #         timeout=600,
# #         max_workers=2   # VERY IMPORTANT
# #     )
# # )


# resuls = evaluate(
#     dataset,
#     metrics=metrics,
#     llm=judge_llm,
#     embeddings=embedding_model,
#     run_config=RunConfig(
#         timeout=1800,
#         max_workers=1
#     )
# )

# print("\nEvaluation Results")
# print(results)


# # ---------- SAVE RESULTS ----------

# results_df = pd.DataFrame([results])

# results_df.to_csv(
#     "eval/eval_results.csv",
#     index=False
# )

# df_sample.to_csv(
#     "eval/evaluated_subset.csv",
#     index=False
# )

# print("\nSaved evaluation outputs")


# import pandas as pd
# from datasets import Dataset
# import random

# from langchain_huggingface import HuggingFaceEmbeddings
# from ragas.embeddings import LangchainEmbeddingsWrapper

# from ragas import evaluate
# from ragas.run_config import RunConfig

# from ragas.metrics._answer_relevance import AnswerRelevancy
# from ragas.metrics._context_precision import ContextPrecision

# from langchain_ollama import ChatOllama
# from ragas.llms import LangchainLLMWrapper


# # ---------- SETTINGS ----------

# EVAL_PERCENTAGE = 0.08
# RANDOM_SEED = 42

# metrics = [
#     AnswerRelevancy(),
#     ContextPrecision(),
# ]

# embedding_model = LangchainEmbeddingsWrapper(
#     HuggingFaceEmbeddings(
#         # model_name="sentence-transformers/all-MiniLM-L6-v2"
#         model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
#     )
# )

# # ---------- LOAD GENERATED ANSWERS ----------

# df = pd.read_csv("eval/generated_answers.csv")

# df_sample = df.sample(
#     frac=EVAL_PERCENTAGE,
#     random_state=RANDOM_SEED
# )

# print(f"\nEvaluating {len(df_sample)} / {len(df)} questions")


# # ---------- FAST RETRIEVAL METRICS (NO LLM) ----------

# def precision_at_k(context, ground_truth):
#     return int(ground_truth.lower() in context.lower())


# def recall_at_k(context, ground_truth):
#     return int(ground_truth.lower() in context.lower())


# precision_scores = []
# recall_scores = []

# for _, row in df.iterrows():
#     precision_scores.append(
#         precision_at_k(row["context"], row["ground_truth"])
#     )
#     recall_scores.append(
#         recall_at_k(row["context"], row["ground_truth"])
#     )

# retrieval_precision = sum(precision_scores) / len(precision_scores)
# retrieval_recall = sum(recall_scores) / len(recall_scores)

# print("\nRetrieval Metrics (fast evaluation)")
# print(f"Precision: {retrieval_precision:.3f}")
# print(f"Recall: {retrieval_recall:.3f}")


# # ---------- CONVERT TO RAGAS DATASET ----------

# dataset = Dataset.from_list([
#     {
#         "question": row["question"],
#         "contexts": [row["context"]],
#         "answer": row["answer"],
#         "ground_truth": row["ground_truth"]
#     }
#     for _, row in df_sample.iterrows()
# ])


# # ---------- JUDGE MODEL (QWEN LOCAL) ----------

# judge_llm = LangchainLLMWrapper(
#     ChatOllama(
#         model="qwen2.5:3b",
#         temperature=0,
#         format="json"
#     )
# )


# # ---------- RUN RAGAS EVALUATION ----------

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

# print("\nLLM Evaluation Results")
# print(result)


# # ---------- SAVE RESULTS ----------

# results_df = pd.DataFrame([result])
# results_df["retrieval_precision"] = retrieval_precision
# results_df["retrieval_recall"] = retrieval_recall

# results_df.to_csv(
#     "eval/eval_results.csv",
#     index=False
# )

# df_sample.to_csv(
#     "eval/evaluated_subset.csv",
#     index=False
# )

# print("\nSaved evaluation outputs")


# evaluate_subset.py

import pandas as pd
import numpy as np
from datasets import Dataset
from tqdm import tqdm

from langchain_huggingface import HuggingFaceEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import evaluate
from ragas.run_config import RunConfig

from ragas.metrics._answer_relevance import AnswerRelevancy
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._context_precision import ContextPrecision
from ragas.metrics._context_recall import ContextRecall

from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper
from sklearn.metrics.pairwise import cosine_similarity

# ---------- SETTINGS ----------
EVAL_PERCENTAGE = 0.08       # fraction of questions to evaluate
RANDOM_SEED = 42
TOP_K = 5                    # number of top contexts to select

# metrics = [
#     ContextPrecision(),
#     ContextRecall(),
#     AnswerRelevancy(),
#     # ContextPrecision(),
#     # Faithfulness()
# ]

metrics = [
    ContextPrecision(),
    ContextRecall()
]

# ---------- LOAD EMBEDDINGS MODEL ----------
embedding_model = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)

# ---------- LOAD GENERATED ANSWERS ----------
df = pd.read_csv("eval/generated_answers.csv")

df_sample = df.sample(
    frac=EVAL_PERCENTAGE,
    random_state=RANDOM_SEED
)

print(f"Evaluating {len(df_sample)} / {len(df)} questions")

# ---------- COMPUTE EMBEDDINGS FOR CONTEXTS ----------
# Extract all unique contexts
all_contexts = df["context"].unique()
context_embeddings = embedding_model.embed_documents(list(all_contexts))

# ---------- SELECT TOP-K CONTEXTS PER QUESTION ----------
ragas_dataset_list = []

for _, row in tqdm(df_sample.iterrows(), total=len(df_sample)):
    question = row["question"]
    answer = row["answer"]
    ground_truth = row["ground_truth"]

    # Embed the question
    question_emb = embedding_model.embed_query(question)

    # Compute cosine similarity with all context embeddings
    sims = cosine_similarity([question_emb], context_embeddings)[0]
    top_idx = np.argsort(sims)[-TOP_K:][::-1]  # descending order
    top_contexts = [all_contexts[i] for i in top_idx]

    ragas_dataset_list.append({
        "question": question,
        "contexts": top_contexts,
        "answer": answer,
        "ground_truth": ground_truth
    })

dataset = Dataset.from_list(ragas_dataset_list)

# ---------- JUDGE MODEL (QWEN) ----------
# judge_llm = LangchainLLMWrapper(
#     ChatOllama(
#         model="qwen2.5:3b",
#         temperature=0,
#         format="json"
#     )
# )

judge_llm = LangchainLLMWrapper(
    ChatOllama(
        model="qwen2.5:3b",
        temperature=0,
        format="json",
        num_predict=256
    )
)

# ---------- RUN EVALUATION ----------
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

print("\nEvaluation Results")
print(result)

# ---------- SAVE RESULTS ----------
results_df = pd.DataFrame([result])
results_df.to_csv("eval/eval_results.csv", index=False)
df_sample.to_csv("eval/evaluated_subset.csv", index=False)

print("\nSaved evaluation outputs")