from typing import Optional
from PIL import Image
import base64
from io import BytesIO
import requests
from app.schemas.aval_ai_models import AvalAIModelName
from app.core.config import settings
from app.models.base import AIClient


class AvalAIGeminiClient(AIClient):
    def __init__(self, model_name: AvalAIModelName = "gemini_pro"):
        self.model_name = model_name
        self.api_key = settings.avalai_api_key
        self.base_url = settings.avalai_base_url.rstrip("/").replace("/v1", "")
        print(f"Using AvalAI Gemini model: {self.model_name}")

    def generate(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        base64_image = None
        if image is not None:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(
                buffered.getvalue()).decode("utf-8")

        parts = [{"text": prompt}]
        if base64_image is not None:
            parts.append(
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64_image,
                    },
                }
            )

        payload = {
            "model": self.model_name,
            "contents": [
                {
                    "role": "user",
                    "parts": parts,
                }
            ]
        }

        response = requests.post(
            f"{self.base_url}/v1beta/models/{self.model_name}:generateContent",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=settings.outbound_timeout_seconds,
        )

        response.raise_for_status()
        data = response.json()

        text_output = ""
        candidates = data.get("candidates", [])
        for candidate in candidates:
            parts = candidate.get("content", {}).get("parts", [])
            for part in parts:
                if "text" in part:
                    text_output += part["text"] + "\n"

        return text_output.strip()
