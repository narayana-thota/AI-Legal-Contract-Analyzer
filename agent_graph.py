# ---------------------------------------------------------
# FILE: agent_graph.py (ULTIMATE DECORATOR EDITION)
# ---------------------------------------------------------
import os
import asyncio
import time
import functools
from typing import TypedDict, List
from dotenv import load_dotenv
from clues import get_agent_keywords
from planning import create_execution_plan

# LangChain Imports
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

# --- 1. SETUP ---
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.1,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    task="feature-extraction",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

try:
    vector_store = PineconeVectorStore(index_name=os.getenv("PINECONE_INDEX_NAME"), embedding=embeddings)
except:
    vector_store = None

# --- 2. THE SENIOR DEVELOPER TOOLKIT (DECORATORS) ---

def retry_with_backoff(retries=3, initial_delay=1):
    """
    A Decorator that automatically retries a function if it hits a Rate Limit.
    Usage: Put @retry_with_backoff before any function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e) or "rate limit" in str(e).lower():
                        print(f"      ⚠️ Rate Limit (429). Retrying in {delay}s...")
                        time.sleep(delay)
                        delay *= 2 # Exponential backoff (1s -> 2s -> 4s)
                    else:
                        raise e # If it's a real error, crash.
            print("      ❌ Max retries reached. Returning fallback.")
            return "Analysis unavailable due to high traffic."
        return wrapper
    return decorator

# --- 3. STATE ---
class ContractAnalysisState(TypedDict):
    user_query: str
    plan: List[dict]
    agent_reports: dict    
    executive_summary: str 
    risk_score: int
    risk_summary: str
    confidence_score: float

# --- 4. WORKER NODES (CLEAN & WRAPPED) ---

def planner_node(state: ContractAnalysisState):
    query = state.get("user_query", "")
    try:
        plan = create_execution_plan(query)
    except:
        plan = [{"role": "Legal Agent", "objective": f"Analyze: {query}"}]
    return {"plan": plan}

def risk_scanner_node(state: ContractAnalysisState):
    if not vector_store: return {"risk_score": 0, "risk_summary": "DB Offline"}
    
    # Lightweight Search
    risky_docs = vector_store.similarity_search("liability indemnity termination penalty", k=3)
    context = "\n".join([d.page_content for d in risky_docs])
    
    prompt = f"""
    Act as Risk Officer.
    CONTEXT: {context[:2000]} 
    Evaluate Risk (0-100).
    OUTPUT FORMAT:
    Score: [Number]
    Summary: [1 sentence warning]
    """
    
    # We define an inner function to use the Retry Decorator
    @retry_with_backoff(retries=2)
    def call_risk_llm():
        return llm.invoke([SystemMessage(content=prompt)]).content

    res = call_risk_llm()
    
    score = 50
    summary = "Pending analysis."
    if res and "Score:" in res:
        try: score = int(''.join(filter(str.isdigit, res.split("Score:")[1].split("\n")[0])))
        except: pass
    if res and "Summary:" in res: summary = res.split("Summary:")[1].strip()
        
    return {"risk_score": score, "risk_summary": summary}

def run_agent_task(role: str, objective: str):
    """ Worker Function """
    print(f"   ⚙️  {role}: Analyzing...")
    if not vector_store: return {"report": "Data Unavailable", "confidence": 0.0}

    # Search Logic
    keywords = get_agent_keywords(role)
    unique_docs = {}
    
    for term in keywords:
        try:
            results = vector_store.similarity_search_with_score(term, k=2)
            for doc, score in results:
                if doc.page_content not in unique_docs: unique_docs[doc.page_content] = score
        except: continue
            
    try:
        obj_results = vector_store.similarity_search_with_score(objective, k=2)
        for doc, score in obj_results:
             if doc.page_content not in unique_docs: unique_docs[doc.page_content] = score
    except: pass

    # Context Building
    if unique_docs:
        scores = list(unique_docs.values())
        avg_score = sum(scores) / len(scores) if scores else 0.0
        confidence = min(avg_score, 1.0)
        full_context = "\n\n".join(unique_docs.keys())
        context_text = full_context[:2500] 
    else:
        context_text = "No relevant clauses found."
        confidence = 0.0

    prompt = f"""
    Role: Senior {role}.
    Task: {objective}
    Data: {context_text}
    
    Structure:
    ## 📝 Key Findings
    * [Fact 1]
    * [Fact 2]
    
    ## 💡 Recommendations
    * [Advice 1]
    * [Advice 2]
    """

    # --- THE MAGIC: CLEAN LLM CALL ---
    @retry_with_backoff(retries=3, initial_delay=2)
    def call_agent_llm():
        return llm.invoke([SystemMessage(content=prompt)]).content

    res = call_agent_llm()
    return {"report": res, "confidence": confidence}

# --- 5. COORDINATOR (THROTTLED & PARALLEL) ---
async def coordinator_node(state: ContractAnalysisState):
    plan = state.get("plan", [])
    print(f"\n🚀 COORDINATOR: Synthesizing {len(plan)} reports...")

    # Semaphore limits concurrency to 2 agents at a time
    semaphore = asyncio.Semaphore(2) 

    async def run_task_safe(task):
        async with semaphore:
            loop = asyncio.get_event_loop()
            # Run the agent (The decorator inside handles the retries!)
            result = await loop.run_in_executor(None, run_agent_task, task["role"], task["objective"])
            return result

    tasks = [run_task_safe(t) for t in plan]
    results_list = await asyncio.gather(*tasks)

    # Aggregate
    agent_outputs = {}
    total_conf = 0.0
    combined_text = ""

    for i, out in enumerate(results_list):
        role = plan[i]["role"]
        agent_outputs[role] = out["report"]
        combined_text += f"\n--- {role} ---\n{out['report']}\n"
        total_conf += out["confidence"]

    # Final Summary
    summary_prompt = f"""
    Role: Lead Lawyer.
    Reports: {combined_text[:3000]}
    
    Output Format:
    **Document Type:** [Identity]
    **Executive Insights:**
    * [Insight 1]
    * [Insight 2]
    """
    
    @retry_with_backoff(retries=2)
    def call_summary_llm():
        return llm.invoke([SystemMessage(content=summary_prompt)]).content

    exec_summary = call_summary_llm()

    avg_conf = (total_conf / len(plan)) if plan else 0.0
    display_conf = min(avg_conf * 1.3, 0.99) if avg_conf > 0 else 0.0
    
    return {
        "agent_reports": agent_outputs,     
        "executive_summary": exec_summary,  
        "confidence_score": display_conf
    }

# --- GRAPH BUILD ---
workflow = StateGraph(ContractAnalysisState)
workflow.add_node("Planner", planner_node)
workflow.add_node("Coordinator", coordinator_node)
workflow.add_node("RiskEngine", risk_scanner_node)

workflow.add_edge(START, "Planner")
workflow.add_edge("Planner", "Coordinator")
workflow.add_edge("Planner", "RiskEngine")
workflow.add_edge("Coordinator", END)
workflow.add_edge("RiskEngine", END)

app = workflow.compile()