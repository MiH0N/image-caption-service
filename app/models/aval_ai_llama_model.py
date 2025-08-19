import base64
from io import BytesIO
from typing import List
from PIL import Image
from openai import OpenAI

from app.core.config import settings
from app.models.base import CaptionModel


class AvalAILLaMACaptionModel(CaptionModel):
    def __init__(self, model_name: str = "llama-4-scout-17b-16e-instruct"):
        self.client = OpenAI(
            api_key=settings.avalai_api_key,
            base_url=settings.avalai_base_url,
        )
        self.model_name = model_name 

    def generate_captions(
        self,
        image: Image.Image,
        language: str,
        tone: str,
        context: str | None = None
    ) -> List[str]:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        prompt = (
            f"Generate 4-5 descriptive captions in {language} with a {tone} tone. "
            "Each caption should have a different perspective. No formatting. Just a list."
        )
        if context:
            prompt += f" Context: {context}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )

        return self._extract_captions(response)

    def _extract_captions(self, response) -> List[str]:
        output = ""
        if hasattr(response, "choices") and response.choices:
            for choice in response.choices:
                if choice.message and hasattr(choice.message, "content"):
                    output += choice.message.content + "\n"

        lines = output.strip().splitlines()
        return [line.strip("-•* ") for line in lines if line.strip()]
