from google import genai
import os
import time

MODEL = "gemini-2.5-flash"
DEFAULT_RETRIES = 3
_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


def _is_503(e: Exception) -> bool:
    """判斷例外是否為 503 Service Unavailable。"""
    return "503" in str(e)


def generate(prompt: str, retries: int = DEFAULT_RETRIES) -> str:
    """呼叫 Gemini API 並回傳生成的文字內容，僅 503 時重試。"""
    for attempt in range(1, retries + 1):
        try:
            response = _client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        except Exception as e:
            if _is_503(e) and attempt < retries:
                wait = 2 ** attempt
                print(f"[Retry {attempt}/{retries}] 503 Service Unavailable，{wait}s 後重試...")
                time.sleep(wait)
            else:
                raise
