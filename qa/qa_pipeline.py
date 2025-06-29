from vectorstore.pinecone_client import get_pinecone_index
from llm.gemini_chain import ask_gemini
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant_chunks(query: str, top_k: int = 5, namespace: str = "default") -> list[str]:
    index = get_pinecone_index()
    query_embedding = model.encode(query).tolist()

    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True, namespace=namespace)
    chunks = [match['metadata']['text'] for match in results['matches']]
    return chunks

def answer_question(query: str, namespace: str = "default") -> str:
    context_chunks = retrieve_relevant_chunks(query, namespace=namespace)
    
    print("🔍 Retrieved Chunks:")
    for i, chunk in enumerate(context_chunks):
        print(f"[{i+1}] {chunk[:200]}...\n")

    context = "\n\n".join(context_chunks)
    return ask_gemini(query=query, context=context)
