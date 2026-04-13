from langchain.llms.base import LLM
from typing import Optional, List
import requests
import os


class DeepSeekGatewayLLM(LLM):
    model: str = "DeepSeek-V3.2"

    @property
    def _llm_type(self) -> str:
        return "deepseek_gateway"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager=None,      # ✅ CLAVE PARA LANGCHAIN
        **kwargs,              # ✅ acepta temperature y otros
    ) -> str:
        headers = {
            "X-Gateway-API-Key": os.getenv("API_KEY"),
            "Content-Type": "application/json",
        }

        body = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,  # fijo para RAGAS
        }

        resp = requests.post(
            f"{os.getenv('BASE_URL')}/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=(10, 60),
        )

        resp.raise_for_status()

        return resp.json()["choices"][0]["message"]["content"].strip()
