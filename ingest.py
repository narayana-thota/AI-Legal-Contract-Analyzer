import os
from dotenv import load_dotenv

# Import standard libraries
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

# NEW: Import Local Embeddings (Free & Unlimited)
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load API Keys
load_dotenv()

def ingest_document():
    print("--- STARTING INGESTION PROCESS (LOCAL MODE) ---")
    
    # Step A: Load the PDF
    file_path = "sample_contract.pdf"
    if not os.path.exists(file_path):
        print(f"❌ Error: Could not find {file_path}")
        return

    print(f"1. Loading {file_path}...")
    loader = PyPDFLoader(file_path)
    raw_docs = loader.load()
    print(f"   - Loaded {len(raw_docs)} pages.")

    # Step B: Split Text
    print("2. Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(raw_docs)
    print(f"   - Created {len(chunks)} text chunks.")

    # Step C: Embed and Upload
    print("3. Initializing Local Embeddings (HuggingFace)...")
    # This runs ON YOUR LAPTOP. No API Key needed.
    # It creates vectors of size 768.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    index_name = os.getenv("PINECONE_INDEX_NAME")
    print(f"   - Uploading to index: '{index_name}'...")

    try:
        PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            index_name=index_name
        )
        print("✅ Success! Document ingested and stored in Pinecone.")
    except Exception as e:
        print(f"❌ Error uploading to Pinecone: {e}")

if __name__ == "__main__":
    ingest_document()