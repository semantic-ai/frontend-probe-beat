from .base import Settings


class FastApiConfig(Settings):
    origin: str

    class Config:
        env_prefix = "fastapi_"
