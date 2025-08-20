from abc import ABC, abstractmethod
from PIL import Image


class AIClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, image: Image.Image | None = None) -> str:
        pass
