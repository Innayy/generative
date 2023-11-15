from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Nomopai OpenAI GPT"
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(env_file="../.env", extra="allow")


settings = Settings()
