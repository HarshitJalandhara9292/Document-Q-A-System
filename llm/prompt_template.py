def format_qa_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful assistant. Answer the user's question using ONLY the context provided below.
If the answer is not in the context, reply with "Sorry, I couldn’t find that information in the document."

--- CONTEXT START ---
{context}
--- CONTEXT END ---

Question: {question}
Answer:
"""
