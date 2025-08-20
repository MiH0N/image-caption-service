from typing import Optional
from PIL import Image
from openai import OpenAI

from app.core.config import settings
from app.models.base import AIClient
from app.utils.image import pil_image_to_base64_jpeg


class AvalAILLaMAClient(AIClient):
    def __init__(self, model_name: str = "llama-4-scout-17b-16e-instruct"):
        self.client = OpenAI(
            api_key=settings.avalai_api_key,
            base_url=settings.avalai_base_url,
            timeout=settings.outbound_timeout_seconds,
        )
        self.model_name = model_name 

    def generate(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        contents = [{"type": "text", "text": prompt}]
        if image is not None:
            base64_image = pil_image_to_base64_jpeg(image)
            contents.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                }
            )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": contents,
                }
            ],
        )

        return self._extract_text(response)

    def _extract_text(self, response) -> str:
        output = ""
        if hasattr(response, "choices") and response.choices:
            for choice in response.choices:
                if choice.message and hasattr(choice.message, "content"):
                    output += choice.message.content + "\n"
        return output.strip()
