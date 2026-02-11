# ⚖️ AI Legal Contract Analyzer

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/Orchestration-LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

> **Infosys Springboard Internship Project**
> *An autonomous, multi-agent AI system for automated legal document auditing and risk assessment.*

---

## 🚀 Live Application
**[Click Here to Launch Dashboard](https://narayana-thota-ai-legal-contract-analyzer-app-dzwx7o.streamlit.app/)**

*Note: The backend runs on serverless infrastructure. Please allow 30-60 seconds for the initial cold start.*

---

## 📄 Project Overview
The **AI Legal Contract Analyzer** is an enterprise-grade document intelligence platform designed to streamline legal reviews. By leveraging **Retrieval-Augmented Generation (RAG)** and **Multi-Agent Architectures**, the system ingests complex legal agreements to execute parallel audits across privacy, finance, and compliance domains.

Unlike standard chatbots, this system utilizes a **Graph-based orchestration engine (LangGraph)** to coordinate specialized AI agents, ensuring higher accuracy and reduced hallucinations for critical business use cases.

## ✨ Key Features
* **🤖 Multi-Agent Orchestration:** Deploys specialized agents (Legal, Financial, Compliance) to analyze contracts from distinct perspectives simultaneously.
* **🔍 Advanced RAG Pipeline:** Powered by **Pinecone Vector DB** and **Hugging Face Embeddings** for high-precision semantic search.
* **📊 Dynamic Risk Scoring:** Auto-calculates an aggregate risk score (0-100) based on detected anomalies and missing standard terms.
* **⚡ Real-Time Visualization:** Interactive Streamlit dashboard featuring confidence metrics, risk heatmaps, and executive summaries.
* **🛡️ Microservices Architecture:** Decoupled **FastAPI** backend for heavy AI computation, separate from the frontend UI.

## 🏗️ Technical Architecture
The application follows a modular microservices pattern:

1.  **Ingestion Layer:** PDF parsing and chunking via `pypdf`.
2.  **Embedding Layer:** Semantic vectorization using `sentence-transformers`.
3.  **Storage Layer:** Serverless vector storage in `Pinecone`.
4.  **Reasoning Layer:** `LangGraph` supervisor managing agent workflows.
5.  **Presentation Layer:** `Streamlit` UI with `Plotly` charts.

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit, Plotly |
| **Backend API** | FastAPI, Uvicorn |
| **LLM Engine** | Groq (Llama-3-70b) |
| **Orchestration** | LangChain, LangGraph |
| **Vector DB** | Pinecone |
| **Deployment** | Render (Backend), Streamlit Cloud (Frontend) |

## 💻 Installation & Setup
Follow these steps to run the project locally.

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/narayana-thota/AI-Legal-Contract-Analyzer.git](https://github.com/narayana-thota/AI-Legal-Contract-Analyzer.git)
    cd AI-Legal-Contract-Analyzer
    ```

2.  **Initialize Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory containing the following API credentials:
    ```env
    GROQ_API_KEY=your_groq_api_key
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_INDEX_NAME=your_index_name
    HUGGINGFACEHUB_API_TOKEN=your_hf_token
    ```

5.  **Execution**
    The application requires two concurrent terminal sessions.

    *Terminal 1 - Backend Service:*
    ```bash
    uvicorn api:app --reload --port 8000
    ```

    *Terminal 2 - Frontend Interface:*
    ```bash
    streamlit run app.py
    ```

## Licensing

This project is distributed under the MIT License. Refer to the LICENSE file for further details.

---

**Author:**
Thota Om Sada Siva Venkata Narayana

**Affiliation:**
Infosys Springboard Intern - Batch 2026