from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

try:
    from vector_store.chroma_store import get_vector_store, has_documents
    from utils.config import GROQ_API_KEY, GROQ_MODEL
except ImportError:
    from backend.vector_store.chroma_store import get_vector_store, has_documents
    from backend.utils.config import GROQ_API_KEY, GROQ_MODEL


def get_answer(query: str):
    if not query or not query.strip():
        raise RuntimeError("Please enter a question to query your documents.")

    if not has_documents():
        raise RuntimeError(
            "No documents are indexed yet. Upload a PDF first, then ask a question."
        )

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    if not GROQ_API_KEY:
        raise RuntimeError(
            "No Groq API key found. Please add GROQ_API_KEY to your .env file."
        )

    try:
        llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0.2,
            groq_api_key=GROQ_API_KEY,
            max_retries=1,
            timeout=30,
        )

        system_prompt = (
            "You are an AI assistant that answers questions based strictly on the "
            "provided context. If the answer is not in the context, say "
            "'I cannot find the answer in the provided documents.' "
            "When the answer is found, keep it concise and grounded in the retrieved text.\n\n"
            "Context: {context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": query})

        answer = response["answer"].strip()
        source_docs = response.get("context", [])
        sources = []
        seen_sources = set()
        for doc in source_docs:
            source_name = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page")
            label = f"{source_name} (page {page + 1})" if isinstance(page, int) else source_name
            if label not in seen_sources:
                seen_sources.add(label)
                sources.append(label)

        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise RuntimeError(f"Groq request failed: {str(e)[:200]}")
