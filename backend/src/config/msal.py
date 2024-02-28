from .base import Settings


class MSALConfig(Settings):
    enabled: bool = True
    client_id: str = ""
    issuer: str = ""

    class Config:
        env_prefix = "msal_"
