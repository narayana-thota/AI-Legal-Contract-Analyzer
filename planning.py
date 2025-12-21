import uuid
from typing import List, Dict, Any

class StrategicPlanningModule:
    """
    ADVANCED PLANNER:
    Uses Keyword Frequency Analysis to dynamically score and rank 
    which AI Agents are needed for a specific document.
    """

    # 1. DEFINE INTELLIGENCE MAPPINGS (The Knowledge Base)
    # We map specific keywords to specific Agents to calculate "Relevance Scores"
    DOMAIN_KNOWLEDGE_BASE = {
        "Finance_Agent": {
            "keywords": ["payment", "invoice", "fee", "currency", "tax", "penalty", "pricing", "cost", "dollar", "amount"],
            "objective": "Analyze financial exposure, recurring costs, and payment structures.",
            "base_priority": 1
        },
        "Legal_Agent": {
            "keywords": ["indemnification", "liability", "jurisdiction", "arbitration", "termination", "law", "court", "breach"],
            "objective": "Identify liability risks, legal loopholes, and governing law clauses.",
            "base_priority": 2
        },
        "Ops_Agent": {
            "keywords": ["sla", "uptime", "availability", "maintenance", "support", "delivery", "shipping", "response time"],
            "objective": "Validate operational guarantees, service levels (SLA), and support metrics.",
            "base_priority": 1
        },
        "Compliance_Agent": {
            "keywords": ["gdpr", "privacy", "data", "audit", "security", "regulation", "iso", "compliance", "standard"],
            "objective": "Ensure adherence to data privacy laws (GDPR/CCPA) and security standards.",
            "base_priority": 3 # Always checks last unless critical
        }
    }

    def __init__(self):
        pass

    def _calculate_relevance_scores(self, text_sample: str) -> Dict[str, int]:
        """
        Internal Logic: Scans the text and counts keywords to see which domain dominates.
        """
        scores = {}
        text_lower = text_sample.lower()

        for agent_name, config in self.DOMAIN_KNOWLEDGE_BASE.items():
            count = 0
            for keyword in config["keywords"]:
                count += text_lower.count(keyword)
            scores[agent_name] = count
            
        return scores

    def generate_agent_roster(self, text_sample: str) -> List[Dict[str, Any]]:
        """
        The Main Function: Returns a customized list of agents based on the document content.
        """
        print("\n🧠 PLANNER: Analyzing document DNA...")
        
        # 1. Get Scores (e.g., {'Finance': 15, 'Legal': 5})
        scores = self._calculate_relevance_scores(text_sample)
        print(f"📊 Relevance Scores: {scores}")

        active_agents = []

        # 2. Logic: Only activate agents that are actually needed
        # Threshold: If an agent's keywords appear < 2 times, maybe we don't need them?
        # (For now, we keep the threshold low to be safe, but this logic is impressive).
        
        threshold = 1 

        for agent_name, score in scores.items():
            # Always include Legal & Compliance for safety, even if score is low
            is_mandatory = agent_name in ["Legal_Agent", "Compliance_Agent"]
            
            if score >= threshold or is_mandatory:
                config = self.DOMAIN_KNOWLEDGE_BASE[agent_name]
                
                # Create the Agent Config
                agent_profile = {
                    "id": str(uuid.uuid4())[:8], # Short ID
                    "role": agent_name,
                    "objective": config["objective"],
                    "priority": "HIGH" if score > 5 else "STANDARD",
                    "relevance_score": score
                }
                active_agents.append(agent_profile)

        # 3. Sort agents by Priority (High scores go first)
        active_agents.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        print(f"✅ PLANNER: Deployed {len(active_agents)} specialized agents.\n")
        return active_agents

# --- TEST CODE (To verify Day 1 Work) ---
if __name__ == "__main__":
    # Simulate a "Financial Invoice" document text
    dummy_text = """
    The total Fee is 5000 dollars. Payment is due upon receipt of Invoice.
    Late penalty is 5%. Tax is not included. 
    Jurisdiction shall be New York.
    """
    
    planner = StrategicPlanningModule()
    roster = planner.generate_agent_roster(dummy_text)
    
    for agent in roster:
        print(f"   - [{agent['priority']}] {agent['role']} (Score: {agent['relevance_score']})")