# RAG Document Chunking Experiment


document = """
Artificial intelligence is transforming many industries.
Machine learning allows computers to learn patterns from data.

Natural language processing enables computers to understand
and process human language.

Computer vision allows machines to understand images and videos.

Large language models can generate and understand human-like text.

Retrieval Augmented Generation combines information retrieval
with large language models to provide more relevant answers.

RAG systems retrieve relevant information from external
documents before generating an answer.
"""


# Chunk size
chunk_size = 200

# Chunk overlap
chunk_overlap = 50


chunks = []


start = 0


while start < len(document):

    end = start + chunk_size

    chunk = document[start:end]

    chunks.append(chunk.strip())

    start += chunk_size - chunk_overlap


print("Original document length:", len(document))

print("Number of chunks:", len(chunks))


print("\nChunks:")
print("=" * 60)


for i, chunk in enumerate(chunks):

    print(f"\nChunk {i + 1}")
    print("-" * 60)
    print(chunk)