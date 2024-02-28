from typing import Annotated

from azure_ad_verify_token import verify_jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .msal import MSALConfig


config = MSALConfig()

bearer_scheme = HTTPBearer(auto_error=False)


async def validate_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    if not config.enabled:
        return

    if credentials is None:
        raise HTTPException(403, detail="Missing bearer token")

    token = credentials.credentials

    azure_ad_app_id = config.client_id
    azure_ad_issuer = config.issuer
    azure_ad_jwks_uri = "https://login.microsoftonline.com/common/discovery/keys"

    verify_jwt(
        token=token,
        valid_audiences=[azure_ad_app_id],
        issuer=azure_ad_issuer,
        jwks_uri=azure_ad_jwks_uri,
        verify=False,
    )
