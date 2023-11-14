from pydantic_settings import BaseSettings


class FastApiConfig(BaseSettings):
    origin: str

    class Config:
        env_prefix = "fastapi_"
