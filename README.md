# 🤖 Product RAG Assistant

A Retrieval-Augmented Generation (RAG) application for answering questions about a product catalog.

This project combines semantic search, vector retrieval, structured filtering, query routing, and LLM-based answer generation to provide grounded answers from product data.

---

## 🚀 Features

- Text embeddings
- Semantic search
- FAISS vector search
- Cosine similarity
- Metadata filtering
- Query intent detection
- Structured product queries
- Hybrid retrieval
- LLM-based answer generation
- Grounded responses
- Similarity threshold
- RAG evaluation
- Streamlit web interface

---

## 🏗️ Architecture

```text
                         User Query
                              │
                              ▼
                       Query Router
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Structured Query          Semantic Query
                 │                         │
                 ▼                         ▼
              Pandas                    FAISS
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                    Retrieved Products
                              │
                              ▼
                       Context Builder
                              │
                              ▼
                         RAG Generator
                              │
                              ▼
                        Final Answer
                              │
                              ▼
                       Streamlit UI
🧠 Models
Embedding Model
all-MiniLM-L6-v2

Embedding dimension:

384
Generation Model
google/flan-t5-small
🛠️ Technologies
Python
PyTorch
Hugging Face Transformers
Sentence Transformers
FAISS
Pandas
Scikit-learn
Streamlit
📂 Project Structure
RAG_Project/
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
⚙️ Installation

Activate the project environment:

conda activate rag-engineer

Install the required dependencies:

pip install -r requirements.txt
▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

You can then ask questions about the product catalog.

💬 Example Questions
Price Queries
Which product is the cheapest laptop?
Which is the most expensive laptop?
Category Queries
Show me smartphones
Which headphones are available?
Semantic Queries
Which laptop is good for programming?
Which laptop is suitable for professional work?
I need a laptop for programming and productivity.
🔍 How Retrieval Works

Product information is converted into numerical embeddings using the Sentence Transformers model.

The embeddings are normalized and stored in a FAISS index.

For a semantic query:

User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Relevant Products
    ↓
Context
    ↓
LLM
    ↓
Answer

The system uses normalized vectors with FAISS inner-product search to approximate cosine similarity.

🔀 Hybrid Retrieval

The system does not use semantic search for every type of question.

The query router detects the user's intent.

Structured queries

For example:

Which product is the cheapest laptop?

The system uses:

Query Router
    ↓
cheapest
    ↓
Pandas
    ↓
Minimum Price

For:

Which is the most expensive laptop?

The system uses:

Query Router
    ↓
most_expensive
    ↓
Pandas
    ↓
Maximum Price
Semantic queries

For example:

Which laptop is good for programming?

The system uses:

Query Router
    ↓
semantic_search
    ↓
FAISS
    ↓
Relevant Products
    ↓
LLM

This hybrid architecture improves reliability by using structured data operations for exact questions and vector search for semantic questions.

🧩 Query Router

The query router currently supports these intents:

cheapest
most_expensive
category_listing
semantic_search

Example:

Which product is the cheapest laptop?

becomes:

Intent: cheapest
Category: Laptop
📊 Evaluation

Run the RAG evaluation with:

python -m experiments.evaluate_rag

The evaluation tests:

Structured price queries
Category queries
Semantic retrieval
Multi-product retrieval

The evaluation compares the system's answer against expected product information.

🛡️ Grounding

The generator is instructed to answer using the retrieved context.

The system also applies a similarity threshold to reject weak semantic matches.

If relevant information cannot be retrieved, the system can return:

I don't have enough information to answer this.

This helps reduce unsupported answers.

⚠️ Model Limitations

This project uses:

google/flan-t5-small

as a lightweight generation model.

Because it is a relatively small model, complex multi-product reasoning may not always be perfect.

To improve reliability, exact operations such as:

Cheapest product
Most expensive product
Category listing

are handled programmatically rather than relying entirely on the LLM.

A larger instruction-tuned model could be used in the future for stronger natural-language generation.

🎯 What This Project Demonstrates

This project demonstrates practical AI Engineering and RAG concepts:

Embeddings
Semantic similarity
Vector search
FAISS
Metadata filtering
Query routing
Hybrid retrieval
Structured retrieval
Context construction
LLM generation
Grounded generation
Retrieval evaluation
Streamlit application development
🔄 RAG Pipeline

The complete pipeline is:

Products Dataset
       ↓
Product Documents
       ↓
Embeddings
       ↓
FAISS Index
       ↓
       ┌──────────────────────┐
       │      User Query      │
       └──────────┬───────────┘
                  ↓
            Query Router
                  ↓
       ┌──────────┴──────────┐
       ↓                     ↓
 Structured              Semantic
 Retrieval               Retrieval
       ↓                     ↓
    Pandas                 FAISS
       │                     │
       └──────────┬──────────┘
                  ↓
          Retrieved Context
                  ↓
            RAG Generator
                  ↓
            Final Answer
                  ↓
           Streamlit UI
🚀 Future Improvements

Possible future improvements include:

Larger instruction-tuned LLM
Better query classification
More advanced metadata filters
Reranking retrieved documents
Conversation memory
Chat history
Multiple document sources
PDF/document ingestion
Persistent vector database
Cloud deployment
RAG observability and monitoring
👨‍💻 Author

Ajmal

AI Engineer Learning Portfolio