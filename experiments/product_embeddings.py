import pandas as pd
from sentence_transformers import SentenceTransformer


# Load dataset
df = pd.read_csv(
    "data/products.csv"
)


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Convert products into text documents
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


# Generate embeddings
embeddings = model.encode(
    documents
)


print("Number of documents:", len(documents))

print(
    "Embedding shape:",
    embeddings.shape
)


# Show first product
print("\nFirst Product:")
print("=" * 60)
print(documents[0])


# Show first embedding
print("\nFirst Product Embedding:")
print("=" * 60)
print(embeddings[0])

print("\nEmbedding dimension:", len(embeddings[0]))