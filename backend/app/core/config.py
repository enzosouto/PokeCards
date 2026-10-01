from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = ""
    the_card_api_key: str = ""
    trawl_api_key: str = ""
    pokemontcg_api_key: str = ""
    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
