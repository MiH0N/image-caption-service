from enum import Enum

class AvalAIModelName(str, Enum):
    gpt_4o = "gpt-4o"
    gemini_pro = "gemini-2.5-flash-lite"
    llama  = "llama-4-scout-17b-16e-instruct"