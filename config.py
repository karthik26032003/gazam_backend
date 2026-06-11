from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # WhatsApp Cloud API
    access_token: str
    phone_number_id: str
    waba_id: str
    app_id: str
    verify_token: str
    app_secret: str

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Anthropic (kept for future use)
    anthropic_api_key: str = ""

    # Local LLM (Gemma via vLLM, OpenAI-compatible)
    local_llm_url: str = "http://164.52.198.104:8049/v1"

    # Gazam External API
    gazam_api_base_url: str = ""
    gazam_api_key: str = ""


settings = Settings()
