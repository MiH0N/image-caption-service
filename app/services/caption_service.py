from app.models.aval_ai_gemini_model import AvalAIGeminiClient
from app.models.aval_ai_model import AvalAIClient
from app.models.aval_ai_llama_model import AvalAILLaMAClient
from app.models.dummy_model import DummyClient
from app.models.base import AIClient
from app.models.blip_model import BlipClient
from app.schemas.caption import CaptionRequestProperty
from app.schemas.aval_ai_models import AvalAIModelName 
from PIL import Image
from typing import List
from app.utils.prompt import build_caption_prompt, build_hashtag_prompt, build_elements_prompt

MODEL_REGISTRY: dict[str, AIClient] = {
  "dummy": DummyClient(),
  "blip": BlipClient(),
  "gpt4o": AvalAIClient(model_name=AvalAIModelName.gpt_4o),
  "gemini_pro": AvalAIGeminiClient(model_name=AvalAIModelName.gemini_pro.value),
  "llama": AvalAILLaMAClient(AvalAIModelName.llama.value),
}

def generate_caption_logic(request: CaptionRequestProperty, image: Image.Image) -> List[str]:
  client = MODEL_REGISTRY.get(request.model_name)
  prompt = build_caption_prompt(
    language=request.language,
    tone=request.tone,
    context=request.context,
    min_captions=4,
    max_captions=5,
    format_style="plain",
  )
  output = client.generate(prompt=prompt, image=image)
  lines = [line.strip() for line in output.splitlines() if line.strip()]
  clean = [line.strip("-•* 1234567890.\t") for line in lines]
  # keep only up to 5
  return clean[:5]


def generate_hashtags_logic(request: CaptionRequestProperty, image: Image.Image) -> List[str]:
  client = MODEL_REGISTRY.get(request.model_name)
  prompt = build_hashtag_prompt(
    language=request.language,
    tone=request.tone,
    context=request.context,
    count=10,
  )
  output = client.generate(prompt=prompt, image=image)
  # split by space, filter to words starting with '#'
  tokens = [t for t in output.replace("\n", " ").split(" ") if t]
  hashtags = [t for t in tokens if t.startswith("#")]
  return hashtags[:10]


def generate_elements_logic(request: CaptionRequestProperty, image: Image.Image) -> List[str]:
  client = MODEL_REGISTRY.get(request.model_name)
  prompt = build_elements_prompt(language=request.language)
  output = client.generate(prompt=prompt, image=image)
  items = [s.strip() for s in output.replace("\n", ",").split(",") if s.strip()]
  return items[:20]
