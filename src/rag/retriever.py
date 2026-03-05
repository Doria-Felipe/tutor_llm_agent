from src.embeddings.model import get_model
import chromadb

client = chromadb.PersistentClient(path="./chroma_easy_german")
col = client.get_or_create_collection("easy_german_a1_multi",
                                      metadata={"hnsw:space": "cosine"})
_model = get_model()
id2title = {}

def clean_context(ctx: str) -> str:
    """Cleaning some spilt garbage from the transcripts

    Args:
        ctx (str): The actual context from the transcripts

    Returns:
        str: the cleaned context
    """
    return "\n".join([line for line in ctx.split("\n")
                      if not ("|" in line and "[" in line)])

def return_context(query: str, k: int = 3):
    """Retrieve top-k transcript chunks for a query

    Args:
        query (str): The user question
        k (int, optional): number of videos to return. Defaults to 3.

    Returns:
        _type_: What our agent will see as context
    """
    q_emb = _model.encode([query], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=q_emb, n_results=k)
    ctx = []

    for meta, doc in zip(res["metadatas"][0], res["documents"][0]):
        vid = meta.get("video_id")
        title = meta.get("title") or id2title.get(vid) or vid or "Unknown"
        ctx.append(f"{title} [{meta.get('start',0):.1f}s–{meta.get('end',0):.1f}s]{doc}")
    return "\n\n".join(ctx)

def return_context_by_video_ids(query: str, video_ids: list, k: int = 3):
    """Retrieve top-k transcript chunks for a query, limited to a list of video_ids.

    Args:
        query (str): The user question
        video_ids (list): a list of video ids where we want to make the search
        k (int, optional): number of videos to return. Defaults to 3.

    Returns:
        _type_: What our agent will see as context
    """
    q_emb = _model.encode([query], normalize_embeddings=True).tolist()

    res = col.query(
        query_embeddings=q_emb,
        n_results=k,
        where={"video_id": {"$in": video_ids}}
    )

    ctx = []
    for meta, doc in zip(res["metadatas"][0], res["documents"][0]):
        ctx.append(doc)

    return "\n\n".join(ctx)