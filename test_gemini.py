
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

if not api_key:
    print("ERROR: GEMINI_API_KEY is missing from .env")
else:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: Gemini API is working"
        )
        print("SUCCESS: Gemini API responded")
        print("Model:", model)
        print("Response:", response.text)
    except Exception as e:
        print("FAILED: Gemini API request failed")
        print(type(e).__name__, str(e))
