import pandas as pd


# Load product dataset
df = pd.read_csv(
    "data/products.csv"
)


print("Dataset loaded successfully.")

print("Number of products:", len(df))

print("Columns:", list(df.columns))


# Convert each product into a text document
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


print("\nNumber of documents:", len(documents))


# Display first document
print("\nFirst Product Document:")
print("=" * 60)
print(documents[0])
print("=" * 60)