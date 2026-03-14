from langchain_groq import ChatGroq

from utils.config import GROQ_API_KEY, GROQ_MODEL


def main():
    print(f"Groq key loaded: {bool(GROQ_API_KEY)}")
    print(f"Chat model: {GROQ_MODEL}")

    if not GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY in backend/.env")

    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.2,
        groq_api_key=GROQ_API_KEY,
        max_retries=1,
        timeout=30,
    )
    response = llm.invoke("Reply with exactly: Groq chat is working.")

    print("Chat test passed.")
    print(response.content)


if __name__ == "__main__":
    main()
