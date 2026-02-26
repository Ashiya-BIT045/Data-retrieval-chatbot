# Agentic Data Retrieval Chatbot

A production-ready AI search system powered by local Mistral (via Ollama), PostgreSQL, and Elasticsearch.

## Prerequisites

1. **Ollama**: Install from [ollama.com](https://ollama.com) and pull Mistral:
   ```bash
   ollama pull mistral
   ```

> [!TIP]
> **Zero-Config Mode**: This system features an automatic "Fallback Driver". If you don't have PostgreSQL or Elasticsearch installed, it will automatically use **SQLite** and **Local JSON** stores so you can test the Agent immediately!

2. **PostgreSQL** (Optional): If running, the system prefers it.
3. **Elasticsearch** (Optional): If running, the system prefers it.

## Setup

1. **Clone and Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file (optional, defaults are set in `app/config.py`):
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=chatbot_db
   ELASTICSEARCH_URL=http://localhost:9200
   ```

3. **Ingest Data**:
   This script will load the Excel files into both databases.
   ```bash
   python -m app.data_loader
   ```

## Running the System

1. **Start the Backend (FastAPI)**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Start the Frontend (Streamlit)**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

Enter natural language queries in the search bar, such as:
- "Software engineers in Dubai"
- "Data scientists in USA"
- "Product managers in Business field"

The LLM will extract the structural parameters and query both PostgreSQL and Elasticsearch independently.
