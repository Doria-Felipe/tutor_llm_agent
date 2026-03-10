import json
from datasets import Dataset
from langchain_community.chat_models import ChatOllama
from ragas.llms import LangchainLLMWrapper
from ragas import evaluate
from ragas.metrics.collections import faithfulness, answer_relevancy
from src.rag.hybrid_retriever import return_context
from src.agent.german_agent import german_agent
from src.llm.client import get_llm

judge_llm = LangchainLLMWrapper(
    ChatOllama(model="llama3.1", temperature=0)
)

llm = get_llm("llama3.1")

with open("data/eval_questions.json") as f:
    questions = json.load(f)

data = []

for q in questions:

    question = q["question"]

    context = return_context(question, k=3)

    answer = german_agent(
        llm=llm,
        user_query=question,
        ctx=context,
        mode="tutor",
        level="a1"
    )

    data.append({
        "question": question,
        "contexts": [context],
        "answer": answer,
        "ground_truth": q["ground_truth"]
    })


dataset = Dataset.from_list(data)

# results = evaluate(
#     dataset,
#     metrics=[
#         faithfulness,
#         answer_relevancy
#     ]
# )

results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy
    ],
    llm=judge_llm
)

print(results)