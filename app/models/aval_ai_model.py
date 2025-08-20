from typing import Optional
from PIL import Image
from openai import OpenAI
from app.models.base import AIClient
from app.schemas.aval_ai_models import AvalAIModelName 
from app.core.config import settings
from app.utils.image import pil_image_to_base64_jpeg

class AvalAIClient(AIClient):
  def __init__(self, model_name: AvalAIModelName = "gpt-4o"):
    self.client = OpenAI(
        api_key=settings.avalai_api_key,
        base_url=settings.avalai_base_url,
        timeout=settings.outbound_timeout_seconds,
    )
    self.model_name = model_name 
    print(f"Using AvalAI model: {self.model_name}")

  def generate(self, prompt: str, image: Optional[Image.Image] = None) -> str:
    contents = [
      {"type": "input_text", "text": prompt},
    ]
    if image is not None:
      base64_image = pil_image_to_base64_jpeg(image)
      contents.append(
        {
          "type": "input_image",
          "image_url": f"data:image/jpeg;base64,{base64_image}",
        }
      )

    response = self.client.responses.create(
      model=self.model_name,
      input=[
        {
          "role": "user",
          "content": contents,
        }
      ],
    )

    if hasattr(response, "output_text") and isinstance(response.output_text, str):
      return response.output_text

    output_text = ""
    if response.output and isinstance(response.output, list):
      for item in response.output:
        if (
          getattr(item, "type", None) == "message"
          and getattr(item, "content", None)
          and isinstance(item.content, list)
        ):
          for content_part in item.content:
            if getattr(content_part, "type", None) == "output_text":
              output_text += content_part.text + "\n"

    return output_text.strip()
