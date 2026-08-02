import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    OPENAI_SDK_AVAILABLE = False

class LLMProvider:
    """
    Direct OpenAI SDK LLM Provider Abstraction (No LangChain).
    Decoupled interface supporting future Claude, Gemini, or local model providers.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
        self.api_base = os.getenv("OPENAI_API_BASE", None)

        self.client = None
        if self.api_key and OPENAI_SDK_AVAILABLE:
            kwargs = {"api_key": self.api_key}
            if self.api_base:
                kwargs["base_url"] = self.api_base
            self.client = OpenAI(**kwargs)

    def generate_response(self, system_prompt: str, user_text: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                response_format={"type": "json_object"},
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"[LLMProvider Warning]: OpenAI SDK error: {e}")
            return None
