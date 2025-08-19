from abc import ABC, abstractmethod
from typing import List
from PIL import Image

class CaptionModel(ABC):
    @abstractmethod
    def generate_captions(self, image: Image.Image, language: str, tone: str, context: str | None = None) -> List[str]:
        pass
