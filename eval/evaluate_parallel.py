import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics.collections import (
    faithfulness,
    answer_relevancy,
)

from concurrent.futures import ThreadPoolExecutor

from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper


judge_llm = LangchainLLMWrapper(
    ChatOllama(model="llama3.1", temperature=0)
)


df = pd.read_csv("eval/generated_answers.csv")


def evaluate_row(row):

    dataset = Dataset.from_list([{
        "question": row["question"],
        "contexts": [row["context"]],
        "answer": row["answer"],
        "ground_truth": row["ground_truth"]
    }])

    # result = evaluate(
    #     dataset,
    #     metrics=[
    #         faithfulness,
    #         answer_relevancy
    #     ],
    #     llm=judge_llm
    # )
    
    results = evaluate(
    dataset,
    metrics=[
        faithfulness(),
        answer_relevancy(),
        context_precision(),
        context_recall()
    ],
    llm=judge_llm
)

    return {
        "question": row["question"],
        "faithfulness": result["faithfulness"],
        "answer_relevancy": result["answer_relevancy"]
    }


with ThreadPoolExecutor(max_workers=6) as executor:

    results = list(executor.map(
        evaluate_row,
        df.to_dict("records")
    ))


results_df = pd.DataFrame(results)

results_df.to_csv("eval/eval_results.csv", index=False)

print("Evaluation complete")