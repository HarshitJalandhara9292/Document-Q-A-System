import os
import google.generativeai as genai
from llm.prompt_template import format_qa_prompt
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(query: str, context: str) -> str:
    prompt = format_qa_prompt(context, query)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini Error] {e}"
