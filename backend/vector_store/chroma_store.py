from functools import lru_cache
import shutil

from langchain_cohere import CohereEmbeddings

try:
    from utils.config import (
        CHROMA_DB_DIR,
        COHERE_API_KEY,
        COHERE_EMBEDDING_MODEL,
        get_collection_name,
    )
except ImportError:
    from backend.utils.config import (
        CHROMA_DB_DIR,
        COHERE_API_KEY,
        COHERE_EMBEDDING_MODEL,
        get_collection_name,
    )


@lru_cache(maxsize=1)
def get_embeddings():
    if not COHERE_API_KEY:
        raise RuntimeError(
            "Missing COHERE_API_KEY. Add it to backend/.env so uploaded documents can be embedded."
        )

    try:
        embeddings = CohereEmbeddings(
            model=COHERE_EMBEDDING_MODEL,
            cohere_api_key=COHERE_API_KEY,
        )
        return embeddings
    except Exception as exc:
        raise RuntimeError(
            f"Failed to initialize Cohere embeddings with model '{COHERE_EMBEDDING_MODEL}'. {exc}"
        ) from exc


@lru_cache(maxsize=1)
def get_vector_store():
    try:
        from langchain_chroma import Chroma
    except ImportError as exc:
        raise RuntimeError(
            "Chroma dependencies are not installed in the active Python environment."
        ) from exc

    return Chroma(
        collection_name=get_collection_name(),
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DB_DIR,
    )


def reset_vector_store():
    shutil.rmtree(CHROMA_DB_DIR, ignore_errors=True)
    get_vector_store.cache_clear()


def add_documents_to_store(docs):
    if not docs:
        raise RuntimeError("No document content was extracted from the uploaded PDF.")

    vector_store = get_vector_store()

    try:
        vector_store.add_documents(docs)
    except Exception as exc:
        message = str(exc)
        if "dimension" in message.lower():
            reset_vector_store()
            vector_store = get_vector_store()
            vector_store.add_documents(docs)
            return
        raise RuntimeError(f"Failed to store document embeddings in Chroma. {message}") from exc


def similarity_search(query, k=4):
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=k)


def has_documents():
    vector_store = get_vector_store()
    collection = getattr(vector_store, "_collection", None)
    if collection is None:
        return False
    return collection.count() > 0
