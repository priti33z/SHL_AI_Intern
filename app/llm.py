import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load variables from .env
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_llm(prompt):
    response = model.generate_content(prompt)
    return response.text