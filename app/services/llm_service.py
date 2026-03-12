import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


def generate_reply(prompt: str):

    try:
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return "LLM error occurred"
