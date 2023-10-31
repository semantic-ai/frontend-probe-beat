from .base import Settings


class MSALConfig(Settings):
    client_id: str
    issuer: str

    class Config:
        env_prefix = "MSAL_"
