from langchain_ollama import ChatOllama

def generate_segmented_summary(text_chunks, model="qwen2.5:0.5b", segment_size=5):
    """
    Generate a summary by segmenting the context into smaller parts.
    :param text_chunks: List of text chunks.
    :param model: The LLM model to use.
    :param segment_size: Number of chunks per segment.
    :return: Comprehensive summary.
    """
    try:
        ollama = ChatOllama(model=model)

        # Summarize each segment
        segment_summaries = []
        for i in range(0, len(text_chunks), segment_size):
            segment = "\n".join(text_chunks[i:i + segment_size])
            prompt = (
                f"Summarize the following text in a clear and detailed way:\n\n{segment}\n\n"
                "Provide the summary in simple and comprehensive language."
            )
            response = ollama.invoke([{"role": "user", "content": prompt}])
            if response.content.strip():
                segment_summaries.append(response.content.strip())

        # Combine segment summaries into a final summary
        combined_context = "\n".join(segment_summaries)
        final_prompt = (
            f"Combine and summarize the following segment summaries into one cohesive summary:\n\n{combined_context}\n\n"
            "Ensure the summary is clear, detailed, and covers all key points."
        )
        final_response = ollama.invoke([{"role": "user", "content": final_prompt}])
        return final_response.content.strip()

    except Exception as e:
        print(f"Error during segmented summarization: {e}")
        return "An error occurred during segmented summarization."
    

