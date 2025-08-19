from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    avalai_api_key: str = "aa-ECEziRAGW0ItBr2IqHJrYYzKlao84NfrDxIbrZfGoOO0KeCz"
    avalai_base_url: str = "https://api.avalai.ir/v1"

    class Config:
        env_file = ".env"

settings = Settings()