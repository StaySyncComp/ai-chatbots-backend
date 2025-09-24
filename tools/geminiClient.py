import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Fix UTF-8 output
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Initialize Gemini Client
try:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    sys.exit(1)
