from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def process_pdf(file_path: str, filename: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Add metadata
    for doc in documents:
        doc.metadata["source"] = filename

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks
