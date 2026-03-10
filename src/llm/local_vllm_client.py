from langchain_openai import ChatOpenAI

def get_llm(
    model_name="qwen2.5:3b",
    temperature=0,
    max_tokens=1024
):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        openai_api_key="EMPTY",
        openai_api_base="http://localhost:11434/v1"
    )