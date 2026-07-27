# rag-mt-evaluator

# Retrieval-Augmented Machine Translation Evaluation (RAG-MTE)

An AI-powered Retrieval-Augmented Machine Translation Evaluation (RAG-MTE) framework that combines Information Retrieval, Traditional MT Evaluation Metrics, and Large Language Models (LLMs) to provide accurate, explainable, and evidence-backed assessment of machine-translated text.

## 📌 Project Overview

Traditional Machine Translation (MT) evaluation metrics such as BLEU, METEOR, TER, chrF++, BERTScore, and COMET mainly rely on reference translations or learned semantic representations. These methods often struggle when multiple valid translations exist, domain knowledge is required, or factual correctness must be verified.

This project introduces a **Retrieval-Augmented Machine Translation Evaluation (RAG-MTE)** framework that retrieves relevant multilingual knowledge from trusted sources before evaluating translation quality. By combining retrieval, semantic reasoning, and explainable scoring, the system produces more reliable and interpretable evaluation results.

---

## 🎯 Objectives

- Evaluate machine translations using external knowledge.
- Support both reference-based and reference-free evaluation.
- Improve translation assessment using Retrieval-Augmented Generation (RAG).
- Detect translation errors using the MQM error taxonomy.
- Generate evidence-backed explanations for every evaluation.
- Produce reliable quality scores for domain-specific translations.

---

## ✨ Key Features

- 🌍 Multi-language Translation Evaluation
- 📚 Retrieval-Augmented Evaluation (RAG)
- 🤖 LLM-based Semantic Reasoning
- 📊 Traditional MT Metrics (BLEU, COMET, BERTScore, etc.)
- 🔍 Hybrid Retrieval (BM25 + Vector Search)
- 🧠 Named Entity & Terminology Verification
- ⚠️ MQM-based Error Detection
- 📈 Score Fusion & Confidence Estimation
- 📝 Explainable Evaluation Reports

---

## 🏗️ System Architecture

```text
User Input
     │
     ▼
Input Validation
     │
     ▼
Linguistic Analysis
     │
     ▼
Query Generation
     │
     ▼
Hybrid Retrieval
(BM25 + Vector Search)
     │
     ▼
Evidence Construction
     │
     ├────────► Traditional Metrics
     │
     └────────► LLM Evaluation
                     │
                     ▼
             MQM Error Detection
                     │
                     ▼
              Score Fusion Engine
                     │
                     ▼
            Final Evaluation Report
```

---

## 🛠️ Technology Stack

### Frontend

- React.js
- Tailwind CSS
- Axios
- React Router

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### NLP

- spaCy
- Stanza
- Indic NLP Library
- Sentence Transformers

### Retrieval

- FAISS
- BM25
- Sentence Embeddings

### LLM

- GPT / Llama / Qwen
- LangChain (if required)

### Database

- PostgreSQL

### Evaluation Metrics

- BLEU
- METEOR
- TER
- chrF++
- BERTScore
- COMET

### Deployment

- Docker
- GitHub

---

## 📂 Project Structure

```
rag-mt-evaluator/
│
├── backend/
├── frontend/
├── datasets/
├── docs/
├── README.md
└── LICENSE
```

---

## 🚀 Development Roadmap

### Phase 1
- Project Setup
- Backend Architecture
- FastAPI
- Database Integration

### Phase 2
- NLP Preprocessing
- Query Generation
- Translation Memory

### Phase 3
- Hybrid Retrieval
- FAISS
- BM25

### Phase 4
- Traditional MT Metrics

### Phase 5
- LLM Evaluation

### Phase 6
- MQM Error Detection

### Phase 7
- Score Fusion

### Phase 8
- React Dashboard

### Phase 9
- Testing & Deployment

---

## 📈 Expected Output

The system generates:

- Overall Translation Quality Score
- Accuracy Score
- Fluency Score
- Terminology Score
- Named Entity Score
- MQM Error Report
- Retrieved Supporting Evidence
- Confidence Score
- Suggested Improved Translation

---

## 📚 Future Enhancements

- Multi-domain evaluation
- Additional language support
- Real-time translation evaluation API
- Interactive dashboard
- Batch translation evaluation
- Research benchmarking

---

## 👨‍💻 Author

**Simran Kumari**

B.Tech Computer Science Engineering  
Internship Project

---

## 📄 License

This project is developed for academic and research purposes.
