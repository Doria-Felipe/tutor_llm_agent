from langchain_core.messages import SystemMessage, HumanMessage
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.memory import ConversationBufferMemory

from src.rag.hybrid_retriever import return_context, clean_context
from src.agent.tools import german_tutor_tool

# -----------------------------
# AGENT
# -----------------------------

def build_agent(llm):

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    tools = [
        german_tutor_tool
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,

        # speed controls
        max_iterations=1,
        early_stopping_method="generate",
        handle_parsing_errors=True
    )

    return agent


def run_agent(agent, user_query: str):

    prompt = f"""
You are a German tutor assistant.

Always answer the user by calling the german_tutor_tool.

User question: {user_query}
"""

    return agent.run(prompt)



# I transformed the following code into a tool

# def german_agent(llm, user_query: str, mode: str='tutor', level: str='a1', k: int=2, ctx: str = None):
#     # if context passed from outside, use it
#     if ctx is None:
#         ctx = clean_context(return_context(user_query, k=k))
#     else:
#         ctx = clean_context(ctx)
        
#     # ctx = ctx[:800]
    
#     templates = {
#         "tutor": f"""
#         You are a supportive German language tutor teaching at {level} level.
#         Follow these steps:
#         1. Answer clearly.
#         2. Explain why the answer is correct.
#         3. Use examples from context {ctx}.
#         4. Give 2–3 German examples with English translations.
#         5. End with one follow-up question.
#         Simple language for {level}.
#         Respond in English + German. Do not mention sources.
#         """,
        
#         "vocab": f"""
#         You are extracting German vocabulary for learners.
#         Topic: {user_query}
#         Level: {level}
#         From the context extract 10 important German words.
#         Rules:
#         - Only output vocabulary
#         - Do not apologize
#         - Do not explain the task
#         - Do not mention the context
#         Format:
#         Word: ...
#         Meaning: ...
#         Example: ...
#         Context:
#         {ctx}
#         """ ,
        
#         "grammar": f"""
#         You are a German grammar trainer ({level} level).
#         Return EXACTLY:
#         - 3 example sentences from context {ctx} (DE-EN)
#         - Short grammar explanation (DE-EN)
#         Max 80 words.
#         """,
        
#         "quiz": f"""
#         You are a German quiz generator ({level} level).
#         Return EXACTLY:
#         - 3 short quiz questions based on the context {ctx} (DE-EN)
#         Max 80 words. No explanations.
#         """    
        
#     }

#     if mode not in templates:
#         raise ValueError(f"Invalid mode: {mode}")

#     system = SystemMessage(content=templates[mode].strip())
#     user = HumanMessage(content=f"Question: {user_query}\n\nContext:\n{ctx}")

#     out = llm.invoke([system, user])
#     return out.content if hasattr(out, "content") else out