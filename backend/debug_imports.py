try:
    from langchain_openai import ChatOpenAI
    print("langchain_openai OK")
except Exception as e:
    print(f"langchain_openai FAILED: {e}")

try:
    from langchain.chains import create_retrieval_chain
    print("create_retrieval_chain (langchain.chains) OK")
except Exception as e:
    print(f"create_retrieval_chain (langchain.chains) FAILED: {e}")

try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
    print("create_stuff_documents_chain (langchain.chains.combine_documents) OK")
except Exception as e:
    print(f"create_stuff_documents_chain (langchain.chains.combine_documents) FAILED: {e}")

try:
    from langchain_core.prompts import ChatPromptTemplate
    print("langchain_core.prompts OK")
except Exception as e:
    print(f"langchain_core.prompts FAILED: {e}")
