import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pinecone import Pinecone

# 1. Load keys
load_dotenv()

print("--- CHECKING CONNECTIONS (FREE MODE) ---")

# 2. Test Google Gemini
try:
    print("Testing Google Gemini...")
    # We use the model found in your list:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    response = llm.invoke("Hello AI, are you working?")
    print(f"✅ Google Gemini Success: {response.content}")
except Exception as e:
    print(f"❌ Google Gemini Error: {e}")

# 3. Test Pinecone
try:
    print("\nTesting Pinecone...")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    indexes = pc.list_indexes()
    print(f"✅ Pinecone Success! Found indexes: {[i.name for i in indexes]}")
except Exception as e:
    print(f"❌ Pinecone Error: {e}")