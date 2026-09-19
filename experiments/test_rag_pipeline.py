from src.rag_pipeline import RAGPipeline


# ==========================================
# Create RAG pipeline
# ==========================================

pipeline = RAGPipeline()


# ==========================================
# Test queries
# ==========================================

queries = [

    "Which product is the cheapest laptop?",

    "Which is the most expensive laptop?",

    "Which laptop is good for programming?"

]


# ==========================================
# Run queries
# ==========================================

for query in queries:

    print("\n" + "=" * 70)
    print("USER QUERY")
    print("=" * 70)

    print(query)


    result = pipeline.run(
        query
    )


    # ======================================
    # Router information
    # ======================================

    print("\n" + "=" * 70)
    print("ROUTER")
    print("=" * 70)

    print(
        "Intent:",
        result["intent"]
    )

    print(
        "Filters:",
        result["filters"]
    )


    # ======================================
    # Retrieved products
    # ======================================

    print("\n" + "=" * 70)
    print("RETRIEVED PRODUCTS")
    print("=" * 70)

    for rank, item in enumerate(
        result["results"],
        start=1
    ):

        print(
            f"\nResult {rank}"
        )

        print(
            item["document"]
        )

        print(
            "Score:",
            item["score"]
        )


    # ======================================
    # Final answer
    # ======================================

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(
        result["answer"]
    )