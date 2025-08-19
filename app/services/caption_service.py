from app.models.aval_ai_gemini_model import AvalAIGeminiCaptionModel
from app.models.aval_ai_model import AvalAICaptionModel
from app.models.aval_ai_llama_model import AvalAILLaMACaptionModel
from app.models.dummy_model import DummyCaptionModel
from app.models.base import CaptionModel
from app.models.blip_model import BlipCaptionModel
from app.schemas.caption import CaptionRequestProperty
from app.schemas.aval_ai_models import AvalAIModelName 
from PIL import Image
from typing import List

MODEL_REGISTRY: dict[str, CaptionModel] = {
  "dummy": DummyCaptionModel(),
  "blip": BlipCaptionModel(),
  "gpt4o": AvalAICaptionModel(model_name=AvalAIModelName.gpt_4o),
  "gemini_pro": AvalAIGeminiCaptionModel(model_name=AvalAIModelName.gemini_pro.value),
  "llama": AvalAILLaMACaptionModel(AvalAIModelName.llama.value),
}

def generate_caption_logic(request: CaptionRequestProperty, image: Image.Image) -> List[str]:
  model = MODEL_REGISTRY.get(request.model_name)
  return model.generate_captions(
    image=image,
    language=request.language,
    tone=request.tone,
    context=request.context
  )
