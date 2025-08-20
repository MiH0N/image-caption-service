from app.models.base import AIClient
from typing import Optional
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=False)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

class BlipClient(AIClient):
  def generate(self, prompt: str, image: Optional[Image.Image] = None) -> str:
    if image is None:
      return ""
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
      out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption