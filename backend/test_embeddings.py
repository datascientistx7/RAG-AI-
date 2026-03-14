from utils.config import COHERE_API_KEY, COHERE_EMBEDDING_MODEL
from vector_store.chroma_store import get_embeddings


def main():
    print(f"Cohere key loaded: {bool(COHERE_API_KEY)}")
    print(f"Embedding model: {COHERE_EMBEDDING_MODEL}")

    embeddings = get_embeddings()
    vector = embeddings.embed_query("hello world")

    print("Embedding test passed.")
    print(f"Vector length: {len(vector)}")


if __name__ == "__main__":
    main()
