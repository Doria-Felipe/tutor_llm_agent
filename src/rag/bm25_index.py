from rank_bm25 import BM25Okapi
import chromadb

client = chromadb.PersistentClient(path="./chroma_easy_german")
col = client.get_collection("easy_german_a1_multi")

docs = col.get()

documents = docs["documents"]
metadatas = docs["metadatas"]

tokenized_corpus = [doc.lower().split() for doc in documents]

bm25 = BM25Okapi(tokenized_corpus)

def bm25_search(query, k=5):
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )[:k]

    results = []

    for idx, _ in ranked:
        results.append({
            "doc": documents[idx],
            "meta": metadatas[idx]
        })

    return results