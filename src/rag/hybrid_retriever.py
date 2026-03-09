# from src.rag.merge import col, _model
from src.rag.vector_store import col, _model
from src.rag.bm25_index import bm25_search
# from src.rag.reranker import rerank


def hybrid_search(query, k=3):

    # semantic search
    q_emb = _model.encode([query], normalize_embeddings=True).tolist()

    vec_res = col.query(
        query_embeddings=q_emb,
        n_results=k
    )

    vector_results = []

    for meta, doc in zip(vec_res["metadatas"][0], vec_res["documents"][0]):
        vector_results.append({
            "doc": doc,
            "meta": meta
        })

    # keyword search
    bm25_results = bm25_search(query, k=k)

    # merge results
    combined = vector_results + bm25_results

    # remove duplicates
    seen = set()
    unique = []

    for r in combined:
        text = r["doc"]
        if text not in seen:
            unique.append(r)
            seen.add(text)

    return unique[:k]

def format_context(results):

    ctx = []

    for r in results:

        meta = r["meta"]
        doc = r["doc"]

        title = meta.get("title", "Unknown")

        ctx.append(
            f"Video: {title}\n"
            f"Time: {meta.get('start',0):.1f}s–{meta.get('end',0):.1f}s\n"
            f"{doc}"
        )

    return "\n\n".join(ctx)

def return_context(query, k=3):

    results = hybrid_search(query, k=k)

    return format_context(results)

# def return_context(query, k=3):

#     # retrieve more candidates
#     results = hybrid_search(query, k=10)
#     # rerank them
#     best = rerank(query, results, top_k=k)

#     return format_context(best)