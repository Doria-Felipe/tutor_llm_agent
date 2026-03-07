from langchain_ollama import ChatOllama

def get_llm(model_name="qwen2.5:3b", temperature=0, num_ctx=1024, num_predict=1024):
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_ctx=num_ctx,
        num_predict=num_predict
    )