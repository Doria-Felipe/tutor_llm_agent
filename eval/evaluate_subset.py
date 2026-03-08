import pandas as pd
import numpy as np
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
    AnswerRelevancy()
]

embedding_model = HuggingFaceEmbeddings(
    # model_name="sentence-transformers/all-MiniLM-L6-v2"
    model_name="intfloat/multilingual-e5-base"
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