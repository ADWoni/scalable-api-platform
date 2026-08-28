from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Scalable Backend & API Platform"
    secret_key: str = "dev-only-change-me-in-real-deployments"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"


settings = Settings()
