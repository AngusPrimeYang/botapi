from google import genai
from google.api_core.exceptions import ServiceUnavailable
import os
import time

MODEL = "gemini-2.5-flash"
DEFAULT_RETRIES = 3
_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


def generate(prompt: str, retries: int = DEFAULT_RETRIES) -> str:
    """呼叫 Gemini API 並回傳生成的文字內容，僅 503 時重試。"""
    for attempt in range(1, retries + 1):
        try:
            response = _client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        except ServiceUnavailable as e:
            if attempt < retries:
                wait = 2 ** attempt
                print(f"[Retry {attempt}/{retries}] 503 Service Unavailable，{wait}s 後重試...")
                time.sleep(wait)
            else:
                raise
