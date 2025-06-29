
import os
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from vectorstore.pinecone_client import get_pinecone_index
from embed.chunking import split_text_into_chunks

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_and_store(text: str, namespace: str = "default") -> str:
    """
    Splits text, embeds chunks, and stores in Pinecone under a given namespace.
    """
    try:
        index = get_pinecone_index()

        chunks = split_text_into_chunks(text)
        vectors = []

        for chunk in chunks:
            embedding = embedding_model.encode(chunk).tolist()
            vector_id = str(uuid4())
            metadata = {"text": chunk}
            vectors.append((vector_id, embedding, metadata))

        index.upsert(vectors=vectors, namespace=namespace)
        return f"✅ Embedded and stored {len(vectors)} chunks to Pinecone (namespace: {namespace})"

    except Exception as e:
        return f"❌ Failed to embed and store: {str(e)}"
