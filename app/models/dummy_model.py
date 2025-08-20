from app.models.base import AIClient
from typing import Optional
from PIL import Image


class DummyClient(AIClient):
    def generate(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        return f"DUMMY OUTPUT -> {prompt[:120]}"
