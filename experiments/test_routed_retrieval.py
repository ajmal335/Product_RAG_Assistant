from src.query_router import QueryRouter
from src.retriever import ProductRetriever


# ==========================================
# Create components
# ==========================================

router = QueryRouter()

retriever = ProductRetriever()


# ==========================================
# Test queries
# ==========================================

queries = [

    "Which product is the cheapest laptop?",

    "Which is the most expensive laptop?",

    "Show me smartphones",

    "Which laptop is good for programming?"

]


# ==========================================
# Process queries
# ==========================================

for query in queries:

    print("\n" + "=" * 60)

    print("QUERY")
    print("=" * 60)

    print(query)


    # --------------------------------------
    # Analyze query
    # --------------------------------------

    analysis = router.analyze(
        query
    )

    intent = analysis["intent"]

    filters = analysis["filters"]

    category = filters.get(
        "category"
    )


    print("\nROUTER")

    print(
        "Intent:",
        intent
    )

    print(
        "Category:",
        category
    )


    # --------------------------------------
    # Select retrieval strategy
    # --------------------------------------

    if intent == "cheapest":

        results = retriever.get_cheapest(
            category
        )

    elif intent == "most_expensive":

        results = retriever.get_most_expensive(
            category
        )

    elif intent == "semantic_search":

        results = retriever.search(
            query,
            top_k=5,
            category=category
        )

    else:

        results = []


    # --------------------------------------
    # Display results
    # --------------------------------------

    print("\nRESULTS")

    for result in results:

        print("\n" + result["document"])

        print(
            "Score:",
            result["score"]
        )