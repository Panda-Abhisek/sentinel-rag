# 🛡️ SentinelRAG

> **An AI Engineering project that builds a production-ready Self-Healing Retrieval-Augmented Generation (RAG) system using FastAPI, LangChain, Qdrant, and open-source LLMs.**

A production-grade Self-Healing Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, Qdrant, and modern AI engineering practices.

SentinelRAG is designed as a long-term AI Engineering portfolio project demonstrating production RAG, evaluation, observability, and autonomous self-healing workflows.
---

# 🚀 Current Status

**Version:** `v0.3.0`

## ✅ Week 1 Completed

### Foundation, Ingestion Pipeline

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

## ✅ Week 2 Completed

### Retrival Pipeline

* Complete Retrieval-Augmented Generation pipeline
* Qdrant semantic retrieval
* Groq-powered grounded answering
* Source citation support
* Modular service-oriented architecture
* Production logging
* Configurable retrieval parameters
* Prompt engineering improvements
* Performance optimizations

### Performance
* First request: Cold start
* Subsequent requests: ~200ms end-to-end

## ✅ Week 3 Completed

### Evaluation Framework

- Retrieval quality evaluation
- Similarity metrics
- Confidence scoring
- Source diversity analysis
- Duplicate chunk detection
- Answer evaluation (LLM-as-a-Judge)
- Hallucination detection
- Structured evaluation reports
- Parallel asynchronous evaluation
- Latency metrics
- Benchmarking script
- Unit tests

---

# 🏗️ Architecture
## Ingestion Pipeline
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
## Retrieval Pipeline
```
                   Question
                        │
                        ▼
                Embedding Model
                        │
                        ▼
             Qdrant Similarity Search
                        │
                        ▼
                Context Builder
                        │
                        ▼
                  Prompt Builder
                        │
                        ▼
                    Groq LLM
                        │
                        ▼
                  Grounded Answer
                        │
                        ▼
                  Source Citations
```
```
                 User Query
                      │
                      ▼
            Semantic Retrieval
                      │
                      ▼
             Context Construction
                      │
                      ▼
             Grounded Generation
                      │
                      ▼
        ┌───────────────────────────────┐
        │                               │
        ▼                               ▼
Answer Evaluation          Hallucination Detection
        │                               │
        └───────────────┬───────────────┘
                        ▼
             Retrieval Evaluation
                        │
                        ▼
             Unified Evaluation Report
                        │
                        ▼
                API Response + Logs
```
---

# 📁 Project Structure

```
backend/

tests/
├── conftest.py
├── evaluation
│   ├── test_confidence_scorer.py
│   ├── test_metrics_calculator.py
│   ├── test_retrieval_evaluator.py
│   └── test_score_level.py

app/
|
├── api
│   ├── dependencies.py
│   ├── document_routes.py
│   ├── health_routes.py
│   └── retrieval_routes.py
|
├── core
│   ├── config.py
│   └── logging_config.py
|
├── embeddings
│    └──embedding_model.py
│   
├── evaluation
│   ├── answer_evaluator.py
│   ├── confidence_scorer.py
│   ├── deepeval_evaluator.py
│   ├── evaluation_logger.py
│   ├── evaluation_service.py
│   ├── hallucination_detector.py
│   ├── metrics.py
│   ├── models.py
│   ├── report_builder.py
│   ├── retrieval_evaluator.py
│   └── score_level.py
|
├── __init__.py
├── main.py
|
├── rag
│   ├── context_builder.py
│   ├── evaluation_prompt_builder.py
│   ├── prompt_builder.py
│   └── source_mapper.py
|
├── schemas
│   ├── index.py
│   └── retrieval.py
|
├── scripts
│   └── benchmark.py
|
├── services
│   ├── document_loader.py
│   ├── evaluation_llm.py
│   ├── index_service.py
│   ├── llm_service.py
│   ├── retrieval_service.py
│   └── text_splitter.py
|
├── utils
│   ├── file_handler.py
│   
└── vectorstore
    └── qdrant_client.py

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

### Evaluation

* NVIDIA API
* Llama 3.3 70B
* LLM-as-a-Judge
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

## Evaluation

* Retrieval confidence scoring
* Similarity statistics
* Source diversity analysis
* Duplicate detection
* Answer quality evaluation
* Hallucination detection
* Structured evaluation reports
* Parallel evaluation pipeline

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

---

## Retrieve Answer

```
POST /query
```
Retrievs answers
### Response

```json
{
  "answer": "string",
  "sources": [
    {
      "page": 0,
      "source": "string",
      "score": 0,
      "content": "string"
    }
  ],
  "evaluation": {
    "retrieval": {
      "confidence": {
        "score": 0,
        "level": "string"
      },
      "metrics": {
        "average_similarity": 0,
        "max_similarity": 0,
        "min_similarity": 0,
        "similarity_std": 0,
        "retrieved_documents": 0,
        "unique_sources": 0,
        "average_chunk_length": 0,
        "duplicate_ratio": 0
      },
      "warnings": [
        "string"
      ]
    },
    "answer": {
      "faithfulness": 0,
      "answer_relevancy": 0,
      "context_utilization": 0,
      "completeness": 0,
      "overall_score": 0
    },
    "hallucination": {
      "hallucination_score": 0,
      "risk_level": "string",
      "grounded": true
    }
  },
  "latency": {
    "retrieval_ms": 0,
    "generation_ms": 0,
    "evaluation_ms": 0,
    "total_ms": 0
  }
}
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
