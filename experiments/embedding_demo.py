from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Example sentences
sentences = [
    "I love machine learning.",
    "Machine learning is fascinating.",
    "I enjoy playing football.",
    "The weather is beautiful today."
]


# Generate embeddings
embeddings = model.encode(
    sentences
)


print("Number of sentences:", len(sentences))

print(
    "Embedding shape:",
    embeddings.shape
)


# Calculate cosine similarity
similarity_matrix = cosine_similarity(
    embeddings
)


print("\nSimilarity Matrix:")
print(similarity_matrix)


# Compare specific sentences
print("\nSimilarity Scores:")

print(
    "Sentence 1 vs Sentence 2:",
    similarity_matrix[0][1]
)

print(
    "Sentence 1 vs Sentence 3:",
    similarity_matrix[0][2]
)

print(
    "Sentence 1 vs Sentence 4:",
    similarity_matrix[0][3]
)