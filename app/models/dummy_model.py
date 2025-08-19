from app.models.base import CaptionModel
from typing import List
from PIL import Image


class DummyCaptionModel(CaptionModel):
    def generate_captions(
        self, image: Image.Image, language: str, tone: str, context: str | None = None
    ) -> List[str]:
        return [
            f"[{language.upper()} - {tone}] Caption 1",
            f"[{language.upper()} - {tone}] Caption 2",
            f"Context: {context or 'None'}",
        ]
