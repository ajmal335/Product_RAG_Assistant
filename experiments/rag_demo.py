from src.retriever import ProductRetriever
from src.generator import RAGGenerator


# ==========================================
# 1. Create retriever
# ==========================================

retriever = ProductRetriever()


# ==========================================
# 2. Create LLM generator
# ==========================================

generator = RAGGenerator()


# ==========================================
# 3. User question
# ==========================================

query = "Which product is the cheapest laptop?"


# ==========================================
# 4. Retrieve relevant products
# ==========================================

results = retriever.search(
    query,
    top_k=5,
    category="laptop"
)


# ==========================================
# 5. Build context
# ==========================================

context = "\n\n".join(
    result["document"]
    for result in results
)


# ==========================================
# 6. Generate answer
# ==========================================

answer = generator.generate(
    query,
    context
)


# ==========================================
# 7. Display results
# ==========================================

print("\n" + "=" * 60)
print("USER QUESTION")
print("=" * 60)

print(query)


print("\n" + "=" * 60)
print("RETRIEVED CONTEXT")
print("=" * 60)


for rank, result in enumerate(
    results,
    start=1
):

    print(f"\nResult {rank}")
    print("-" * 60)

    print(result["document"])

    print(
        "Similarity Score:",
        result["score"]
    )


print("\n" + "=" * 60)
print("RAG ANSWER")
print("=" * 60)

print(answer)