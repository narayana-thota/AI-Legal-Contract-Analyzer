# AI Legal Contract Analyzer

Developed an AI legal analyst using Python and LangChain for pipeline and LangGraph, Gemini for orchestration.

- This system parses PDF contracts to extract key financial terms and stores vectors in Pinecone cloud.

### Technologies Used:
- Python
- LangChain & LangGraph
- Google Gemini (LLM)
- Pinecone (Vector Database)
- HuggingFace (Local Embeddings)

### How to Run:
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API keys to a `.env` file.
4. Run `python ingest.py` to process the contract.
5. Run `python main.py` to start the AI Analyst.