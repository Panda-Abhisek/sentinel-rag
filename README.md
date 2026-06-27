# 🛡️ SentinelRAG

> **An AI Engineering project that builds a production-ready Self-Healing Retrieval-Augmented Generation (RAG) system using FastAPI, LangChain, Qdrant, and open-source LLMs.**

SentinelRAG is designed to go beyond a basic RAG implementation. Instead of simply retrieving documents and generating responses, the long-term goal is to build an autonomous retrieval system capable of validating its own answers, retrying retrieval when necessary, and reducing hallucinations through an evaluation pipeline.

---

# 🚀 Current Status

**Version:** `v0.1.0`

## ✅ Week 1 Completed

* FastAPI backend architecture
* Modular project structure
* PDF upload endpoint
* PDF parsing with PyMuPDF
* Recursive document chunking
* Metadata enrichment
* BAAI BGE embedding model
* Qdrant vector database integration
* Production-style logging
* Configuration using `.env`
* Service-oriented architecture

---

# 🏗️ Architecture

```
                   Upload PDF
                        │
                        ▼
              FastAPI Upload API
                        │
                        ▼
             Temporary File Storage
                        │
                        ▼
               Document Loader
                        │
                        ▼
               Recursive Splitter
                        │
                        ▼
             Metadata Enrichment
                        │
                        ▼
           BGE Embedding Generation
                        │
                        ▼
              Qdrant Vector Store
```

---

# 📁 Project Structure

```
backend/

app/
│
├── api/
│     ├── document_routes.py
│     └── health_routes.py
│
├── core/
│     ├── config.py
│     └── logging_config.py
│
├── embeddings/
│     └── embedding_model.py
│
├── schemas/
│     └── index.py
│
├── services/
│     ├── document_loader.py
│     ├── text_splitter.py
│     └── index_service.py
│
├── utils/
│     └── file_handler.py
│
├── vectorstore/
│     └── qdrant_client.py
│
├── rag/
│
└── main.py
```

---

# ⚙️ Tech Stack

### Backend

* FastAPI
* Pydantic
* Python 3.14

### RAG Framework

* LangChain

### Embedding Model

* BAAI/bge-small-en-v1.5

### Vector Database

* Qdrant

### PDF Processing

* PyMuPDF

### Deployment

* Docker
* Docker Compose

### Planned LLM Providers

* Groq
* Qwen
* DeepSeek

---

# ✨ Features

## Document Processing

* Upload PDF documents
* Automatic document parsing
* Intelligent recursive chunking
* Metadata enrichment
* Temporary file management

## Vector Pipeline

* Local embedding generation
* Embedding normalization
* Vector indexing
* Persistent storage in Qdrant

## Engineering

* Clean architecture
* Modular services
* Structured logging
* Environment-based configuration
* Production-ready project layout

---

# 📡 API

## Upload Document

```
POST /documents/upload
```

Uploads a PDF, generates embeddings, and stores vectors inside Qdrant.

### Response

```json
{
  "status": "success",
  "filename": "FastAPI.pdf",
  "collection": "sentinel_rag",
  "chunks": 395
}
```

---

## Health Check

```
GET /health
```

---

# 🛠️ Running Locally

Clone the repository

```bash
git clone <repository-url>
cd Sentinel_RAG/backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start Qdrant

```bash
docker compose up -d
```

Run the backend

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 🗺️ Roadmap

## ✅ Week 1

* Backend foundation
* PDF ingestion pipeline
* Embedding generation
* Qdrant integration

## 🚧 Week 2

* Semantic retrieval
* Query endpoint
* Context generation
* Groq integration
* Qwen / DeepSeek support

## 📋 Week 3

* LangGraph workflow
* Self-healing retrieval
* Query rewriting
* Critic agent
* Retry mechanism

## 📊 Week 4

* Evaluation metrics
* Observability
* Monitoring
* Production deployment
* Performance optimization

---

# 🎯 Long-Term Goal

SentinelRAG aims to evolve into an autonomous AI retrieval system capable of:

* Detecting unsupported answers
* Automatically rewriting poor search queries
* Retrying retrieval with improved context
* Reducing hallucinations
* Providing explainable and traceable responses
* Serving as a production-grade AI engineering reference project

---

# 📄 License

This project is licensed under the MIT License.
