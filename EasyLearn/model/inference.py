from langchain_ollama import ChatOllama

def generate_segmented_summary(text_chunks, model="qwen2.5:0.5b", segment_size=5):
    ollama = ChatOllama(model=model)
    combined_summary = "\n".join([
        ollama.invoke([{"role": "user", "content": chunk}]).content.strip()
        for chunk in text_chunks[:segment_size]
    ])
    return combined_summary
