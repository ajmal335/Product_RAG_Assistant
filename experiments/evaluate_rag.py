from src.rag_pipeline import RAGPipeline


# ==========================================
# Create RAG pipeline
# ==========================================

pipeline = RAGPipeline()


# ==========================================
# Evaluation Dataset
# ==========================================

test_cases = [

    {
        "query": "Which product is the cheapest laptop?",
        "expected": ["HP Pavilion 15"]
    },

    {
        "query": "Which is the most expensive laptop?",
        "expected": ["MacBook Pro 14"]
    },

    {
        "query": "Show me smartphones",
        "expected": [
            "iPhone 16 Pro",
            "Samsung Galaxy S25",
            "Google Pixel 9"
        ]
    },

    {
        "query": "Which headphones are available?",
        "expected": [
            "Sony WH-1000XM5",
            "Apple AirPods Pro"
        ]
    },

    {
        "query": "Which laptop is good for programming?",
        "expected": [
            "MacBook Pro 14",
            "Dell XPS 15",
            "Lenovo ThinkPad X1 Carbon"
        ]
    }
]


# ==========================================
# Evaluation
# ==========================================

passed = 0


for test_case in test_cases:

    query = test_case["query"]

    expected = test_case["expected"]


    result = pipeline.run(
        query
    )


    answer = result["answer"]


    # ======================================
    # Check expected products
    # ======================================

    matches = [

        product

        for product in expected

        if product.casefold()
        in answer.casefold()

    ]


    is_pass = (
        len(matches) == len(expected)
    )


    if is_pass:

        passed += 1


    # ======================================
    # Display result
    # ======================================

    print("\n" + "=" * 70)

    print("QUERY")
    print("=" * 70)

    print(query)

    print("\nEXPECTED")

    for product in expected:

        print(
            f"- {product}"
        )


    print("\nACTUAL")

    print(answer)


    print(
        "\nRESULT:",
        "PASS" if is_pass else "FAIL"
    )


# ==========================================
# Final Evaluation
# ==========================================

total = len(test_cases)

accuracy = (
    passed / total
) * 100


print("\n" + "=" * 70)

print("FINAL RAG EVALUATION")

print("=" * 70)

print(
    f"Passed: {passed}/{total}"
)

print(
    f"Accuracy: {accuracy:.2f}%"
)