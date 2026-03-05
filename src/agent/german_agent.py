from langchain_core.messages import SystemMessage, HumanMessage
from src.rag.retriever import return_context, clean_context

def german_agent(llm, user_query: str, mode: str='tutor', level: str='a1', k: int=2, ctx: str = None):
    # if context passed from outside, use it
    if ctx is None:
        ctx = clean_context(return_context(user_query, k=k))
    else:
        ctx = clean_context(ctx)
        
    # ctx = ctx[:800]
    
    templates = {
        "tutor": f"""
        You are a supportive German language tutor teaching at {level} level.
        Follow these steps:
        1. Answer clearly.
        2. Explain why the answer is correct.
        3. Use examples from context.
        4. Give 2–3 German examples with English translations.
        5. End with one follow-up question.
        Simple language for {level}.
        Respond in English + German. Do not mention sources.
        """,
        "vocab": f"""
        You are a German vocabulary trainer ({level} level).
        Return EXACTLY:
        - 5 key words (DE-EN)
        - 1 example per word from context (DE-EN)
        Max 80 words. No explanations.
        """,
        "grammar": f"""
        You are a German grammar trainer ({level} level).
        Return EXACTLY:
        - 3 example sentences from context (DE-EN)
        - Short grammar explanation (DE-EN)
        Max 80 words.
        """,
        "quiz": f"""
        You are a German quiz generator ({level} level).
        Return EXACTLY:
        - 3 short quiz questions (DE-EN)
        Max 80 words. No explanations.
        """
    }

    if mode not in templates:
        raise ValueError(f"Invalid mode: {mode}")

    system = SystemMessage(content=templates[mode].strip())
    user = HumanMessage(content=f"Question: {user_query}\n\nContext:\n{ctx}")

    out = llm.invoke([system, user])
    return out.content if hasattr(out, "content") else out