import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END

# Load Environment Variables
load_dotenv()

# --- 1. SETUP CLOUD TOOLS ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vector_store = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings
)

# --- 2. DEFINE THE STATE ---
class ContractAnalysisState(TypedDict):
    """
    The 'Shared Folder' that gets passed between agents.
    """
    contract_id: str
    plan: List[dict]       # The JSON list from the Planner
    final_reports: dict    # Where we store the results

# --- 3. DYNAMIC WORKER AGENT ---
def run_agent_task(state: ContractAnalysisState, agent_config: dict):
    """
    This is a universal function. It becomes whatever agent the Plan tells it to be.
    """
    role = agent_config['role']
    objective = agent_config['objective']
    
    print(f"   ⚙️  Running Agent: {role}...")

    # A. Search Pinecone using the Agent's Objective as the query
    # (Smart move: use the objective to find relevant clauses!)
    docs = vector_store.similarity_search(objective, k=4)
    context_text = "\n\n".join([d.page_content for d in docs])

    # B. Construct the Prompt
    prompt = f"""
    ROLE: You are the {role}.
    OBJECTIVE: {objective}
    
    CONTEXT (Retrieved from Contract):
    {context_text}
    
    TASK:
    Analyze the context and write a concise finding report.
    If no relevant info is found, say 'No significant clauses found.'
    """

    # C. Run AI
    msg = [SystemMessage(content=prompt)]
    res = llm.invoke(msg)
    
    return res.content

def coordinator_node(state: ContractAnalysisState):
    """
    The Manager Node. It loops through the Plan and activates agents one by one.
    """
    print(f"\n🚀 COORDINATOR: Executing Plan with {len(state['plan'])} Agents.")
    
    results = {}
    
    # Loop through the list (Compliance, Legal, etc.)
    for agent in state['plan']:
        report = run_agent_task(state, agent)
        results[agent['role']] = report
        
    # Save to state
    return {"final_reports": results}

# --- 4. BUILD THE GRAPH ---
workflow = StateGraph(ContractAnalysisState)
workflow.add_node("Coordinator", coordinator_node)
workflow.add_edge(START, "Coordinator")
workflow.add_edge("Coordinator", END)
app = workflow.compile()

# --- 5. THE PUBLIC FUNCTION (API CALLS THIS) ---
def analyze_contract_with_graph(plan_json: List[dict]):
    """
    This function triggers the whole process.
    """
    initial_state = {
        "contract_id": "doc_001",
        "plan": plan_json,
        "final_reports": {}
    }
    
    # Run the graph
    final_state = app.invoke(initial_state)
    return final_state['final_reports']