import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

try:
    from models.schemas import QueryRequest, QueryResponse
    from utils.config import UPLOAD_DIR
    from rag.document_processor import process_pdf
    from vector_store.chroma_store import add_documents_to_store
    from services.llm_service import get_answer
except ImportError:
    from backend.models.schemas import QueryRequest, QueryResponse
    from backend.utils.config import UPLOAD_DIR
    from backend.rag.document_processor import process_pdf
    from backend.vector_store.chroma_store import add_documents_to_store
    from backend.services.llm_service import get_answer

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name was provided.")

    filename = os.path.basename(file.filename)
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        chunks = process_pdf(file_path, filename)
        add_documents_to_store(chunks)
        
        return {"message": f"Successfully processed {filename}", "chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        result = get_answer(request.query)
        return QueryResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
