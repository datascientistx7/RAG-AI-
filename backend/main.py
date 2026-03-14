from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from api.routes import router as api_router
    from utils.config import ensure_directories
except ImportError:
    from backend.api.routes import router as api_router
    from backend.utils.config import ensure_directories

app = FastAPI(
    title="RAG AI AI App",
    description="Backend for PDF RAG application using Cohere embeddings and Groq LLMs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    ensure_directories()

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
