import os
from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_gemini_response(prompt: str) -> str:
    try:
        resp = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return resp.text
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"