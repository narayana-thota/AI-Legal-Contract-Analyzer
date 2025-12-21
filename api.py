import shutil
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_community.document_loaders import PyPDFLoader

# IMPORT YOUR MODULES
from planning import StrategicPlanningModule
from agent_graph import analyze_contract_with_graph  # <--- IMPORT THE NEW FILE

app = FastAPI(title="Legal AI Planner API", version="2.0")
planner = StrategicPlanningModule()

@app.post("/analyze_contract")
async def full_contract_analysis(file: UploadFile = File(...)):
    print(f"\n📥 API RECEIVED FILE: {file.filename}")
    
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 1. READ PDF (First 3 pages for Planning)
        print("   Step 1: Scanning Document...")
        loader = PyPDFLoader(temp_filename)
        pages = loader.load()
        text_sample = "".join([p.page_content for p in pages[:3]])
        
        # 2. GENERATE PLAN (Module 2)
        print("   Step 2: Generating Strategic Plan...")
        agent_plan = planner.generate_agent_roster(text_sample)
        
        # 3. EXECUTE GRAPH (Module 3)
        print("   Step 3: Executing AI Agents...")
        final_reports = analyze_contract_with_graph(agent_plan)
        
        # Cleanup
        os.remove(temp_filename)
        
        # 4. RETURN FINAL REPORT
        return {
            "status": "Success",
            "strategy_used": [a['role'] for a in agent_plan],
            "executive_summary": final_reports
        }

    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))