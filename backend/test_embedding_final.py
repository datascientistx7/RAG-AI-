from utils.config import COHERE_API_KEY, COHERE_EMBEDDING_MODEL
from vector_store.chroma_store import get_embeddings


def main():
    print(f"Cohere key loaded: {bool(COHERE_API_KEY)}")
    print(f"Embedding model: {COHERE_EMBEDDING_MODEL}")

    embeddings = get_embeddings()

    samples = [
        "This is a test.",
        "Retrieval augmented generation helps ground answers in documents.",
        "Vector databases store embeddings for similarity search.",
    ]

    for index, sample in enumerate(samples, start=1):
        vector = embeddings.embed_query(sample)
        print(f"Sample {index}: vector length = {len(vector)}")

    print("Cohere embedding smoke test passed.")


if __name__ == "__main__":
    main()
