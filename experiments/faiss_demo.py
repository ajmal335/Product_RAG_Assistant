import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer


# ==========================================
# 1. Load product dataset
# ==========================================

df = pd.read_csv(
    "data/products.csv"
)


# ==========================================
# 2. Load embedding model
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# 3. Convert products into documents
# ==========================================

documents = []

for _, row in df.iterrows():

    document = f"""
Product ID: {row['productid']}
Name: {row['name']}
Category: {row['category']}
Description: {row['description']}
Stock: {row['stock']}
Season: {row['season']}
Price: ${row['price']}
""".strip()

    documents.append(document)


# ==========================================
# 4. Generate embeddings
# ==========================================

embeddings = model.encode(
    documents
)


print("Embedding shape:", embeddings.shape)


# ==========================================
# 5. Convert embeddings to float32
# ==========================================

embeddings = embeddings.astype(
    "float32"
)


# ==========================================
# 6. Create FAISS index
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)


# ==========================================
# 7. Add embeddings to FAISS
# ==========================================

index.add(
    embeddings
)


print("Number of vectors in FAISS:", index.ntotal)


# ==========================================
# 8. Create a search query
# ==========================================

query = "laptop for programming"


# Convert query into embedding
query_embedding = model.encode(
    [query]
).astype("float32")


# ==========================================
# 9. Search FAISS
# ==========================================

k = 3

distances, indices = index.search(
    query_embedding,
    k
)


# ==========================================
# 10. Display results
# ==========================================

print("\nSearch Query:")
print(query)

print("\nTop Results:")
print("=" * 60)


for rank, (distance, idx) in enumerate(
    zip(distances[0], indices[0]),
    start=1
):

    print(f"\nResult {rank}")
    print("-" * 60)

    print(
        documents[idx]
    )

    print(
        "Distance:",
        distance
    )