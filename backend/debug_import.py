import sys
import os

print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
# print(f"Path: {sys.path}")

try:
    import google
    print(f"Google package location: {google.__path__}")
    import google.generativeai
    print(f"GenerativeAI location: {google.generativeai.__file__}")
except Exception as e:
    print(f"Error: {e}")
