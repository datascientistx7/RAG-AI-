# RAG AI Application

This is a modern full-stack application for Retrieval Augmented Generation using Next.js and FastAPI.

## Architecture
- **Frontend**: Next.js (App Router), React, TailwindCSS, Framer Motion
- **Backend**: FastAPI, LangChain, Chroma, OpenAI embeddings

## Setup & Running

### Requirements
- Node.js 18+
- Python 3.9+
- OpenAI API Key

### Backend Setup
1. `cd backend`
2. Create virtualenv: `python -m venv venv`
3. Activate:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Edit `backend/.env` to include your `OPENAI_API_KEY`. (If none is provided, it uses mock responses)
6. Run the server: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

### Frontend Setup
1. `cd frontend`
2. `npm install`
3. Run the dev server: `npm run dev`

### Usage
- Go to `http://localhost:3000`
- Click `Upload PDF` or go to the Documents tab
- Upload a standard PDF file. The backend will parse, chunk, and embed the text into ChromaDB.
- Go to the Chat tab and start asking questions!
