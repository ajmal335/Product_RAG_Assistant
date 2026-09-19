from src.query_router import QueryRouter


router = QueryRouter()


queries = [
    "Which product is the cheapest laptop?",
    "Show me smartphones",
    "Which is the most expensive laptop?",
    "I need headphones",
    "Which laptop is good for programming?"
]


for query in queries:

    result = router.analyze(
        query
    )

    print("\nQuery:")
    print(query)

    print("Analysis:")
    print(result)