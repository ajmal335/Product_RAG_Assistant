# 🤖 Product RAG Assistant

> A Retrieval-Augmented Generation (RAG) system for intelligent product search and question answering.

The **Product RAG Assistant** combines semantic search, vector retrieval, structured filtering, query routing, and large language model generation to answer questions from a product catalog.

The application uses **Sentence Transformers** for embeddings, **FAISS** for vector search, **Hugging Face Transformers** for answer generation, and **Streamlit** for the user interface.

---

## 📌 Project Overview

Traditional keyword search often fails when a user asks a question using different words from those stored in the database.

For example:
> *Which laptop is good for programming?*

Instead of matching only keywords, this system converts the query and product information into embeddings and retrieves products based on semantic similarity.

For exact questions such as:
> *Which product is the cheapest laptop?*

the system uses structured filtering with Pandas rather than relying only on semantic similarity. This creates a hybrid RAG architecture combining semantic and structured retrieval.

---

## ✨ Features

- 🔤 Text embeddings using Sentence Transformers
- 🔎 Semantic similarity search
- 🗂️ FAISS vector search
- 📊 Cosine similarity
- 🏷️ Metadata/category filtering
- 🧠 Query intent detection
- 🔀 Hybrid retrieval
- 📋 Structured product queries
- 🤖 LLM-based answer generation
- 🛡️ Context-grounded responses
- 🎯 Similarity threshold for weak-match filtering
- 📈 RAG evaluation
- 🌐 Streamlit web application

---

## 🏗️ System Architecture

```text
                          ┌─────────────────┐
                          │    User Query   │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Query Router   │
                          └────────┬────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌─────────────────┐           ┌─────────────────┐
          │ Structured Query│           │ Semantic Query  │
          └────────┬────────┘           └────────┬────────┘
                   │                             │
                   ▼                             ▼
              ┌─────────┐                   ┌─────────┐
              │ Pandas  │                   │  FAISS  │
              └────┬────┘                   └────┬────┘
                   │                             │
                   └──────────────┬──────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Retrieved Context│
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   RAG Generator  │
                         │    FLAN-T5       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Final Answer   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Streamlit App   │
                         └──────────────────┘
```

---

## 🔄 RAG Workflow

The complete workflow is:

```text
Product Dataset
      ↓
Product Documents
      ↓
Text Embeddings
      ↓
FAISS Vector Index
      ↓
User Query
      ↓
Query Router
      ↓
Structured / Semantic Retrieval
      ↓
Relevant Product Context
      ↓
LLM
      ↓
Grounded Answer
```

---

## 🧠 Query Routing

The system automatically analyzes the user's question and identifies the appropriate retrieval strategy.

### Supported Intents
- `cheapest`
- `most_expensive`
- `category_listing`
- `semantic_search`

### Example
**User query:**
> *Which product is the cheapest laptop?*

**Router output:**
- **Intent:** `cheapest`
- **Category:** `Laptop`

The system then performs an exact price comparison using the product dataset.

---

## 🔀 Hybrid Retrieval

The system uses two retrieval strategies.

### 1. Structured Retrieval
Used for questions that require exact operations.

**Example:**
> *Which product is the cheapest laptop?*

```text
User Query ──► Query Router ──► cheapest ──► Category Filter ──► Pandas ──► Minimum Price ──► Answer
```

**Another example:**
> *Which is the most expensive laptop?*

```text
User Query ──► Query Router ──► most_expensive ──► Category Filter ──► Pandas ──► Maximum Price ──► Answer
```

### 2. Semantic Retrieval
Used for questions where meaning and relevance are more important than exact filtering.

**Example:**
> *Which laptop is good for programming?*

```text
User Query ──► Query Embedding ──► FAISS Similarity Search ──► Relevant Products ──► Context ──► LLM ──► Answer
```

---

## 🔤 Embeddings

The project uses `all-MiniLM-L6-v2`.

Each product document is converted into a **384-dimensional vector**. These vectors represent the semantic meaning of the product information and are normalized before being stored in FAISS.

---

## 🔎 FAISS Retrieval

FAISS is used for efficient vector similarity search. The project uses `faiss.IndexFlatIP` with normalized vectors.

Because the vectors are normalized, inner-product similarity approximates cosine similarity. The system also applies a similarity threshold to reject very weak semantic matches.

---

## 🤖 Generation Model

The project uses `google/flan-t5-small` as the generation model.

The model receives the retrieved product context and user question and generates the final answer. The generator is instructed to use only the retrieved context.

---

## 🛡️ Grounded Generation

The system follows a simple grounding principle:

```text
User Question + Retrieved Context ──► LLM ──► Grounded Answer
```

The generator is instructed not to use outside information. If relevant information cannot be retrieved, the system returns:

> *"I don't have enough information to answer this."*

---

## 📊 Evaluation

The project includes a RAG evaluation script. Run:

```bash
python -m experiments.evaluate_rag
```

The evaluation covers:
- Structured price queries
- Category queries
- Semantic retrieval
- Multi-product retrieval

The evaluation compares the generated response against expected product information.

---

## 💬 Example Queries

### 💰 Price Queries
- *Which product is the cheapest laptop?*
- *Which is the most expensive laptop?*

### 📱 Category Queries
- *Show me smartphones*
- *Which headphones are available?*

### 💻 Semantic Queries
- *Which laptop is good for programming?*
- *Which laptop is suitable for professional work?*
- *I need a laptop for programming and productivity.*

---

## 🖥️ Streamlit Application

The project includes a Streamlit interface for interacting with the RAG system. Run:

```bash
streamlit run app.py
```

The application provides:
- User query input
- Example questions
- Generated answers
- Query intent information
- Detected filters
- Retrieved product context
- Similarity scores

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Application development |
| **PyTorch** | Deep learning framework |
| **Hugging Face Transformers** | Text generation |
| **Sentence Transformers** | Text embeddings |
| **FAISS** | Vector similarity search |
| **Pandas** | Structured data processing |
| **Scikit-learn** | Machine learning utilities |
| **Streamlit** | Web application |

---

## 📂 Project Structure

```text
Product_RAG_Assistant/
│
├── data/
│   └── products.csv
│
├── src/
│   ├── generator.py
│   ├── query_router.py
│   ├── retriever.py
│   └── rag_pipeline.py
│
├── experiments/
│   ├── chunking_demo.py
│   ├── embedding_demo.py
│   ├── faiss_demo.py
│   ├── product_embeddings.py
│   ├── product_loader.py
│   ├── rag_demo.py
│   ├── test_retriever.py
│   ├── test_router.py
│   ├── test_routed_retrieval.py
│   ├── test_rag_pipeline.py
│   └── evaluate_rag.py
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:ajmal335/Product_RAG_Assistant.git
   ```

2. **Enter the project directory:**
   ```bash
   cd Product_RAG_Assistant
   ```

3. **Activate the Conda environment:**
   ```bash
   conda activate rag-engineer
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

---

## 🧪 Run the Tests

- **Test Query Router:**
  ```bash
  python -m experiments.test_router
  ```

- **Test Retrieval:**
  ```bash
  python -m experiments.test_retriever
  ```

- **Test Routed Retrieval:**
  ```bash
  python -m experiments.test_routed_retrieval
  ```

- **Test Complete RAG Pipeline:**
  ```bash
  python -m experiments.test_rag_pipeline
  ```

- **Run RAG Evaluation:**
  ```bash
  python -m experiments.evaluate_rag
  ```

---

## ⚠️ Model Limitations

This project uses `google/flan-t5-small` as a lightweight generation model. Because it is a relatively small model, complex multi-product reasoning may not always be perfect.

For this reason, exact operations such as:
- Cheapest product
- Most expensive product
- Category listing

are handled programmatically. This prevents the LLM from being responsible for deterministic data operations. A larger instruction-tuned model could improve generation quality for more complex questions.

---

## 🚀 Future Improvements

Potential improvements include:
- Larger instruction-tuned LLM
- Advanced query classification
- More metadata filters
- Document reranking
- Conversation memory & Chat history
- PDF/document ingestion
- Multiple knowledge sources
- Persistent vector database
- Cloud deployment
- RAG observability and monitoring
- Automated evaluation with larger test sets

---

## 🎯 Learning Outcomes

This project demonstrates practical AI Engineering concepts including:
- Embeddings & Semantic similarity
- Vector search & FAISS
- Metadata filtering & Query routing
- Hybrid retrieval & Structured retrieval
- Context construction & LLM generation
- Grounded generation & RAG evaluation
- Streamlit application development

---

## 👨‍💻 Author

**Ajmal**  
*AI Engineer | Python | Machine Learning | Deep Learning | NLP | RAG*
