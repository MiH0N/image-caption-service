from app.models.base import CaptionModel
from typing import List
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=False)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

class BlipCaptionModel(CaptionModel):
    def generate_captions(self, image: Image.Image, language: str, tone: str, context: str | None = None) -> List[str]:
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return [f"{caption}"] 