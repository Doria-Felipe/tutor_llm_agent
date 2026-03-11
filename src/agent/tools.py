from langchain_core.tools import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage
from src.llm.client import get_llm
from src.rag.hybrid_retriever import return_context, clean_context


def german_agent(llm, user_query: str, mode: str = "tutor", level: str = "a1", ctx: str = None):
    """Direct LLM call for German tutor answers"""
    if ctx is None:
        raw_ctx = return_context(user_query, k=2)
        ctx = clean_context(raw_ctx)[:1000]

    templates = {
        "tutor": f"""
        You are a supportive German language tutor teaching at {level} level.
        Follow these steps:
        1. Answer clearly.
        2. Explain why the answer is correct.
        3. Use examples from context {ctx}.
        4. Give 2–3 German examples with English translations.
        5. End with one follow-up question.
        Simple language for {level}.
        Respond in English + German. Do not mention sources.
        """
    }

    system = SystemMessage(content=templates[mode].strip())
    user = HumanMessage(content=user_query)

    response = llm.invoke([system, user])
    return response.content if hasattr(response, "content") else response


class GermanTutorTool(BaseTool):
    """SingleToolAgent for fast German tutor answers"""

    name: str = "german_tutor_tool"
    description: str = "Answers questions about German for learners."

    llm: object
    level: str = "a1"

    # Updated _run() to accept optional context
    def _run(self, query: str, ctx: str = None) -> str:
        return german_agent(llm=self.llm, user_query=query, mode="tutor", level=self.level, ctx=ctx)

    async def _arun(self, query: str, ctx: str = None) -> str:
        raise NotImplementedError


def build_german_tool(llm, level="a1") -> GermanTutorTool:
    """Factory function to create a single-tool agent"""
    return GermanTutorTool(llm=llm, level=level)