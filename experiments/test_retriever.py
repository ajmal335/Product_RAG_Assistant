from src.retriever import ProductRetriever

# Create retriever
retriever = ProductRetriever()


# Test query
query = "laptop for programming"


results = retriever.search(
    query,
    top_k=3
)


print("Query:")
print(query)

print("\nRetrieved Products:")
print("=" * 60)


for rank, result in enumerate(
    results,
    start=1
):

    print(f"\nResult {rank}")
    print("-" * 60)

    print(
        result["document"]
    )

    print(
        "Distance:",
        result["distance"]
    )

    print(
        "Product ID:",
        result["product_id"]
    )