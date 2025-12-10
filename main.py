import os
from typing import TypedDict
from dotenv import load_dotenv

# Import Libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

# 1. Load Keys
load_dotenv()

# 2. Setup the "Brain" (Google Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 3. Setup the "Memory" (Pinecone + HuggingFace)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings
)

# 4. Define the Shared Folder (State)
class AgentState(TypedDict):
    query: str               # The User's Question
    context: str             # The Contract Text found in Pinecone
    finance_report: str      # Report from Finance Agent
    legal_report: str        # Report from Legal Agent
    operations_report: str   # Report from Operations Agent

# 5. Define the Agent Nodes

# --- Node A: The Researcher (Retrieval) ---
def retrieve_node(state: AgentState):
    print(f"\n--- 🔍 SEARCHING PINECONE FOR: '{state['query']}' ---")
    docs = vector_store.similarity_search(state["query"], k=3)
    found_text = "\n\n".join([d.page_content for d in docs])
    print(f"   - Found {len(docs)} relevant clauses.")
    return {"context": found_text}

# --- Node B: Finance Agent ---
def finance_agent(state: AgentState):
    # Only run if context exists
    if not state["context"]: return {"finance_report": "No data found."}
    
    print("--- 💰 FINANCE AGENT ANALYZING ---")
    prompt = """You are a Senior Finance Analyst. 
    Review the contract data below. Your job is to Extract:
    1. Monthly Fees and Total Contract Value.
    2. Payment Terms (e.g., Net 30).
    3. Late Payment Penalties.
    If information is missing, explicitly say 'Not specified'."""
    
    msg = [SystemMessage(content=prompt), HumanMessage(content=state["context"])]
    response = llm.invoke(msg)
    return {"finance_report": response.content}

# --- Node C: Legal Agent ---
def legal_agent(state: AgentState):
    if not state["context"]: return {"legal_report": "No data found."}

    print("--- ⚖️ LEGAL AGENT ANALYZING ---")
    prompt = """You are a Senior Corporate Lawyer. 
    Review the contract data below. Your job is to Extract:
    1. Termination conditions (Notice period).
    2. Liability Caps (Max dollar amount).
    3. Governing Law location.
    If information is missing, explicitly say 'Not specified'."""
    
    msg = [SystemMessage(content=prompt), HumanMessage(content=state["context"])]
    response = llm.invoke(msg)
    return {"legal_report": response.content}

# --- Node D: Operations Agent ---
def operations_agent(state: AgentState):
    if not state["context"]: return {"operations_report": "No data found."}

    print("--- ⚙️ OPERATIONS AGENT ANALYZING ---")
    prompt = """You are an Operations Manager. 
    Review the contract data below. Your job is to Extract:
    1. Service Level Agreements (SLAs) or Uptime guarantees.
    2. Support response times.
    3. Deliverables.
    If information is missing, explicitly say 'Not specified'."""
    
    msg = [SystemMessage(content=prompt), HumanMessage(content=state["context"])]
    response = llm.invoke(msg)
    return {"operations_report": response.content}

# 6. Build the Workflow Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("Researcher", retrieve_node)
workflow.add_node("Finance", finance_agent)
workflow.add_node("Legal", legal_agent)
workflow.add_node("Operations", operations_agent)

# Connect Edges
workflow.add_edge(START, "Researcher")
workflow.add_edge("Researcher", "Finance")
workflow.add_edge("Finance", "Legal")
workflow.add_edge("Legal", "Operations")
workflow.add_edge("Operations", END)

# Compile
app = workflow.compile()

# 7. Run the Application (INTERACTIVE MODE)
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 LEGAL AI AGENT: ONLINE")
    print("Type 'exit' or 'quit' to stop.")
    print("="*50)

    while True:
        try:
            # 1. Get User Input
            user_question = input("\n📝 Ask a question about the contract: ")
            
            # 2. Check for Exit
            if user_question.lower() in ["exit", "quit", "q"]:
                print("Goodbye! 👋")
                break
            
            # 3. Check for empty input
            if not user_question.strip():
                continue

            print(f"\n🚀 Analyzing...")
            
            # 4. Run the Pipeline
            result = app.invoke({"query": user_question})
            
            # 5. Print Results
            print("\n" + "="*60)
            
            # Only print reports if they contain useful info
            if "Not specified" not in result['finance_report']:
                print(f"💵 FINANCE REPORT:\n{result['finance_report']}\n")
                print("-" * 40)
                
            if "Not specified" not in result['legal_report']:
                print(f"⚖️ LEGAL REPORT:\n{result['legal_report']}\n")
                print("-" * 40)
                
            if "Not specified" not in result['operations_report']:
                print(f"⚙️ OPERATIONS REPORT:\n{result['operations_report']}")
                
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error: {e}")