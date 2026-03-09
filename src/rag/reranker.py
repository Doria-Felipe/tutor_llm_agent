from sentence_transformers import CrossEncoder

# Load once
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, results, top_k=3):
    """
    results: list of {"doc":..., "meta":...}
    """

    pairs = [(query, r["doc"]) for r in results]

    scores = reranker.predict(pairs)

    scored = list(zip(results, scores))

    ranked = sorted(
        scored,
        key=lambda x: x[1],
        reverse=True
    )

    return [r[0] for r in ranked[:top_k]]