import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

# Always load the backend-local .env file, regardless of the shell working directory.
load_dotenv(ENV_FILE)

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("groq")
COHERE_API_KEY = (
    os.getenv("COHERE_API_KEY")
    or os.getenv("cohir")
    or os.getenv("cohere")
)

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
COHERE_EMBEDDING_MODEL = os.getenv("COHERE_EMBEDDING_MODEL", "embed-english-v3.0")

CHROMA_DB_DIR = os.path.abspath(
    os.path.join(BASE_DIR, os.getenv("CHROMA_DB_DIR", "./chroma_db"))
)
UPLOAD_DIR = os.path.abspath(
    os.path.join(BASE_DIR, os.getenv("UPLOAD_DIR", "./uploads"))
)


def get_collection_name() -> str:
    model_slug = COHERE_EMBEDDING_MODEL.replace("/", "_").replace(".", "_").replace("-", "_")
    return f"rag_documents_{model_slug}"


def ensure_directories():
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
