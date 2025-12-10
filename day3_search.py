import os
from dotenv import load_dotenv

# Import Libraries
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load Keys
load_dotenv()

def test_retrieval():
    print("--- STARTING RETRIEVAL TEST (DAY 3) ---")
    
    # Step A: Setup the Connection
    # We MUST use the exact same embedding model we used for Ingestion
    print("1. Initializing Local Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    # Step B: Connect to the Index
    index_name = os.getenv("PINECONE_INDEX_NAME")
    print(f"2. Connecting to Pinecone Index: '{index_name}'...")
    
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )

    # Step C: Ask a Question
    query = "What are the payment terms?"
    print(f"\n3. Searching for: '{query}'")
    
    # This asks Pinecone: "Give me the 2 paragraphs most similar to this question"
    results = vector_store.similarity_search(query, k=2)
    
    # Step D: Print Results
    print(f"\n--- RESULTS FOUND: {len(results)} ---")
    for i, doc in enumerate(results):
        print(f"\n[Result {i+1}]")
        print(f"Content: {doc.page_content[:300]}...") # Print first 300 chars
        print("-" * 40)

if __name__ == "__main__":
    test_retrieval()