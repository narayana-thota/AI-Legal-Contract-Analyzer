import os
import time
from dotenv import load_dotenv
from tqdm import tqdm # Progress bar
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_pinecone import PineconeVectorStore

# 1. Load Environment Variables
load_dotenv()

def ingest_data():
    print("\n🚀 STARTING CLOUD INGESTION...")

    # 2. Load the PDF
    pdf_path = "sample_contract.pdf" # Make sure this file exists!
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' not found.")
        return

    print(f"📄 Loading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"   - Loaded {len(documents)} pages.")

    # 3. Split Text (Chunks)
    print("✂️  Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    all_docs = text_splitter.split_documents(documents)
    print(f"   - Created {len(all_docs)} text chunks.")

    # 4. Initialize Google Embeddings (The "Translator")
    print("🧠 Initializing Google Embeddings (Dimension: 768)...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 5. Batch Upload to Pinecone (The "Safety" Loop)
    index_name = os.getenv("PINECONE_INDEX_NAME")
    print(f"☁️  Uploading to Pinecone Index: '{index_name}'...")
    
    batch_size = 50 
    
    # Using tqdm for a professional progress bar
    for i in tqdm(range(0, len(all_docs), batch_size), desc="   Processing Batches"):
        batch = all_docs[i : i + batch_size]
        
        # Upload batch
        PineconeVectorStore.from_documents(
            batch,
            index_name=index_name,
            embedding=embeddings
        )
        
        # Sleep to be polite to Google API
        time.sleep(1)

    print("\n✅ SUCCESS! The contract is now in the Cloud Brain.")

if __name__ == "__main__":
    ingest_data()