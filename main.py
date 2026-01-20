# main.py
# Module 6: The CEO (User Input -> Planner -> Agent Graph -> Report)

import json
import time
from planning import create_execution_plan
from agent_graph import analyze_contract_with_graph

def main():
    print("\n🤖 LEGAL AI AGENT: System Online")
    print("================================================")
    print("   Brain: Groq (Llama-3)")
    print("   Memory: Pinecone + Hugging Face")
    print("================================================")
    
    # 1. Get User Input
    user_query = input("\n📝 Enter your request (e.g., 'Check for financial risks'): ")
    
    # Default if user hits Enter without typing
    if not user_query.strip():
        user_query = "Analyze this contract for all major risks and liabilities."
        print(f"   (No input detected. Using default: '{user_query}')")

    # --- STEP 1: PLANNING (The Architect) ---
    print("\n\n--- 🏗️  PHASE 1: PLANNING ---")
    start_time = time.time()
    
    # Call the Planner Module
    plan = create_execution_plan(user_query)
    
    if not plan:
        print("❌ Error: The Planner failed to generate a valid list. Exiting.")
        return

    # Show the User what the AI is planning to do
    print(f"✅ Plan Approved: {len(plan)} tasks created.")
    for i, step in enumerate(plan, 1):
        print(f"   {i}. {step['role']}: {step['objective']}")

    # --- STEP 2: EXECUTION (The Agents) ---
    print("\n\n--- 🚀 PHASE 2: EXECUTION ---")
    
    # Call the Graph Module
    final_report = analyze_contract_with_graph(plan)
    
    execution_time = time.time() - start_time

    # --- STEP 3: FINAL REPORT ---
    print("\n\n================================================")
    print(f"📊 FINAL INTELLIGENCE REPORT (Generated in {execution_time:.2f}s)")
    print("================================================")
    
    if not final_report:
        print("⚠️  No results returned. The agents might not have found relevant data.")
    
    for role, report in final_report.items():
        print(f"\n👤 AGENT: {role.upper()}")
        print("-" * 40)
        # Clean up the output to make it readable
        print(report.strip())
        print("-" * 40)

    print("\n✅ Job Complete.")

if __name__ == "__main__":
    main()