from pydantic import BaseModel
from typing import Optional, Union

from enum import Enum

class ModelNameOption(str, Enum):
  DUMMY = "dummy"
  BLIP = "blip"
  gpt4o = "gpt4o"
  gemini_pro = "gemini_pro"
  llama = "llama"


class CaptionRequestProperty(BaseModel):
  model_name: ModelNameOption
  language: str
  tone: str
  context: Optional[str] = None

