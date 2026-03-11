from langchain_classic.memory import ConversationBufferMemory
from src.agent.tools import build_german_tool

def build_agent(llm, level="a1"):
    """Return a single-tool German tutor agent"""
    tool = build_german_tool(llm, level=level)
    return tool