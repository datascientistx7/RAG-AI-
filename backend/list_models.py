import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_1")
genai.configure(api_key=api_key)

print("Listing models...")
try:
    for m in genai.list_models():
        print(f"Name: {m.name}, Supported: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error: {e}")
