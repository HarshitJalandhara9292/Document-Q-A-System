import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

# Init Pinecone object (not global init)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_pinecone_index():
    index_name = os.getenv("PINECONE_INDEX_NAME")
    return pc.Index(index_name)
