# 🛡️ SentinelRAG

> **An AI Engineering project that builds a production-ready Self-Healing Retrieval-Augmented Generation (RAG) system using FastAPI, LangChain, LangGraph, Qdrant, and open-source LLMs.**

A production-grade Self-Healing Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, LangGraph, Qdrant, and modern AI engineering practices.

SentinelRAG is designed as a long-term AI Engineering portfolio project demonstrating production RAG, evaluation, observability, and autonomous self-healing workflows.
---

# 🚀 Current Status

**Version:** `v0.5.0`

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

## ✅ Week 4 Completed

### Self-Healing Retrieval

- Autonomous self-healing retrieval pipeline
- Evaluation-driven retry decisions
- Query rewriting using an LLM
- Intelligent retry strategy
- Automatic answer selection
- Healing policy engine
- Healing report generation
- End-to-end healing orchestration
- Production-grade dependency injection
- Comprehensive unit tests
- Integration tests

## ✅ Week 5 Completed

### LangGraph Agentic Workflow

- LangGraph-based agentic workflow orchestration
- Planner agent — LLM-driven retrieve-vs-rewrite routing decision
- Critic agent — answer quality evaluation with finish/retry routing
- Query rewriting node with retry tracking
- Multi-candidate answer generation and accumulation across attempts
- Answer selector — score-based candidate selection using faithfulness, relevancy, completeness, and hallucination score
- Reflection agent — explainable reasoning for the selected answer
- Conditional routing with retry limits (max_retries: 2)
- Modular node architecture with dependency-injected context via `SentinelContext`
- State graph visualization script (`visualize_graph.py`)

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
## Evaluation Pipeline
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
# Self-Healing Pipeline
```
                  User Query
                      │
                      ▼
             Initial Retrieval
                      │
                      ▼
              Retrieval Evaluation
                      │
                      ▼
             Answer Evaluation
                      │
                      ▼
          Hallucination Detection
                      │
                      ▼
               Healing Policy
                      │
             Retry Required?
               ┌───────────┐
          No   │           │ Yes
               ▼           ▼
        Return Answer   Rewrite Query
                             │
                             ▼
                      Query Rewriter
                             │
                             ▼
                    Second Retrieval
                             │
                             ▼
                     Second Evaluation
                             │
                             ▼
                     Answer Selector
                             │
                             ▼
                     Healing Report
                             │
                             ▼
                     Final API Response
```
# LangGraph Agentic Workflow
```
                  User Query
                       │
                       ▼
                   Planner
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
          Retrieve            Rewrite
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
                   Generate
                       │
                       ▼
                  Evaluate
                       │
                       ▼
                   Critic
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
         Selector            Rewrite
             │              (retry +1)
             │                   │
             ▼                   │
        Reflection               │
             │                   │
             └───────────────────┘
                       │
                       ▼
                Final Answer
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
├── langgraph
│   ├── __init__.py
│   ├── constants.py
│   ├── dependencies.py
│   ├── edges.py
│   ├── graph.py
│   ├── models.py
│   ├── router.py
│   ├── state.py
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── critic_node.py
│   │   ├── evaluation_node.py
│   │   ├── generation_node.py
│   │   ├── planner_node.py
│   │   ├── reflection_node.py
│   │   ├── retrieval_node.py
│   │   ├── rewrite_node.py
│   │   └── selector_node.py
│   └── prompts/
│       ├── critic.txt
│       ├── planner.txt
│       └── reflection.txt
|
├── __init__.py
├── main.py
|
├── rag
│   ├── context_builder.py
│   ├── evaluation_prompt_builder.py
│   ├── prompt_builder.py
│   ├── rewrite_prompt_builder.py
│   └── source_mapper.py
|
├── schemas
│   ├── index.py
│   └── retrieval.py
|
├── scripts
│   ├── benchmark.py
│   ├── test_graph.py
│   └── visualize_graph.py
|
├── services
│   ├── answer_selector_service.py
│   ├── critic_service.py
│   ├── document_loader.py
│   ├── evaluation_llm.py
│   ├── generation_service.py
│   ├── graph_service.py
│   ├── index_service.py
│   ├── llm_service.py
│   ├── planner_service.py
│   ├── query_rewriter_service.py
│   ├── reflection_service.py
│   ├── response_service.py
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
* LangGraph

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

### Self-Healing

* Automatic query rewriting
* Evaluation-driven retry strategy
* Intelligent healing policy
* Automatic answer comparison
* Hallucination-aware answer selection
* Healing report generation
* Graceful fallback on retry failures
* End-to-end self-healing orchestration

### Agentic Workflow

* LangGraph state graph orchestration
* Planner agent — retrieve-vs-rewrite routing
* Critic agent — quality-driven retry decisions
* Reflection agent — explainable answer selection
* Multi-candidate answer accumulation
* Conditional routing with retry limits
* Dependency-injected node context
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

## LangGraph Agentic Workflow

* State graph orchestration via LangGraph
* Planner agent for query routing decisions
* Critic agent for quality-driven retry
* Automatic query rewriting on retry
* Multi-candidate answer management
* Score-based answer selection
* Reflection-based explainability
* Conditional routing with configurable retry limits
* Dependency-injected context per execution
* ASCII and Mermaid graph visualization

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
  "response": {
    "answer": "...",
    "sources": [],
    "evaluation": {},
    "latency": {}
  },
  "healing": {
    "original_query": "...",
    "rewritten_query": "...",
    "healing_attempted": true,
    "healing_success": true,
    "retry_count": 1,
    "retry_reason": "low_answer_quality",
    "selected_answer": "healed",
    "winner_reason": "higher_answer_quality",
    "original_score": 0.63,
    "healed_score": 0.91,
    "latency_overhead_ms": 812
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

## ✅ Week 3

* Retrieval evaluation
* Answer evaluation
* Hallucination detection
* Confidence scoring
* Parallel evaluation pipeline
* Structured evaluation reports

## ✅ Week 4

* Self-healing retrieval
* Query rewriting
* Healing policy engine
* Retry strategy
* Answer selection
* Healing reports
* Unit tests
* Integration tests

## ✅ Week 5

* LangGraph workflow
* Multi-agent orchestration
* Planner agent
* Critic agent
* Query rewriting node
* Multi-candidate answer selection
* Reflection agent
* State graph visualization

## 🚧 Week 6

* Observability & monitoring
* Production deployment preparation
* Performance benchmarking
* Frontend integration

---

# 🎯 Long-Term Goal

SentinelRAG aims to evolve into an autonomous AI retrieval system capable of:

* Evaluating every generated answer
* Detecting unsupported responses
* Automatically rewriting ambiguous queries
* Retrying retrieval using improved search queries
* Selecting the best answer from multiple candidates
* Producing transparent healing reports
* Reducing hallucinations
* Providing explainable and traceable responses
* Serving as a production-grade AI engineering reference project
---

# 📄 License

This project is licensed under the MIT License.
