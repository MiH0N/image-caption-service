from typing import List
from PIL import Image
import base64
from io import BytesIO
from openai import OpenAI
from app.models.base import CaptionModel
from app.schemas.aval_ai_models import AvalAIModelName 
from app.core.config import settings

class AvalAICaptionModel(CaptionModel):
  def __init__(self, model_name: AvalAIModelName = "gpt-4o"):
    self.client = OpenAI(
        api_key=settings.avalai_api_key,
        base_url=settings.avalai_base_url,
        timeout=settings.outbound_timeout_seconds,
    )
    self.model_name = model_name 
    print(f"Using AvalAI model: {self.model_name}")

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

    prompt_text = (
      "Generate a descriptive caption for the uploaded image that clearly describes its main content in a natural, generate 4-5 captions, each with a different perspective. "
      f"with a {tone} tone, in {language}. If context is given, consider it."
      "For each caption, provide a single string without any additional formatting. "
      "Present the captions as a numbered list in the response. "
      "Do not include any extra characters or symbols between captions. "
      "Example format:"
      "1. Caption 1\n"
      "2. Caption 2\n"
      "3. Caption 3\n"
    )
    if context:
      prompt_text += f" Context: {context}"

    response = self.client.responses.create(
      model=self.model_name,
      input=[
        {
          "role": "user",
          "content": [
            {"type": "input_text", "text": prompt_text},
            {
              "type": "input_image",
              "image_url": f"data:image/jpeg;base64,{base64_image}",
            },
          ],
        }
      ],
    )

    output_text = ""
    if hasattr(response, "output_text"):
        output_text = response.output_text
    else:
      if response.output and isinstance(response.output, list):
        for item in response.output:
          if (
            item.type == "message"
            and item.content
            and isinstance(item.content, list)
          ):
            for content_part in item.content:
              if content_part.type == "output_text":
                output_text += content_part.text + "\n"

    cleaned = output_text.strip().splitlines()
    cleaned = [line.strip("-•* ") for line in cleaned if line.strip()]
    return cleaned
