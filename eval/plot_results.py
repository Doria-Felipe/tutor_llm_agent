import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("eval/eval_results.csv")

# metrics = [
#     "faithfulness",
#     "answer_relevancy",
#     "context_precision",
#     "context_recall"
# ]
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


values = [df[m][0] for m in metrics]


plt.bar(metrics, values)

plt.title("RAG Evaluation Scores")

plt.ylim(0, 1)

plt.ylabel("Score")

plt.show()