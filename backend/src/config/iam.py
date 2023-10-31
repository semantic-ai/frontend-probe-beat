from typing import Optional

from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes

from .azure_ad import verify_azure_jwt


class OAuthHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        token = await super().__call__(request)

        if token is None:
            token = request.query_params.get("token", None)
            if token is not None:
                return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        return token


async def validate_user(
    security_scopes: SecurityScopes,
    creds: Optional[HTTPAuthorizationCredentials] = Depends(
        OAuthHTTPBearer(auto_error=False)
    ),
) -> None:
    if creds is None:
        raise HTTPException(403, detail="Missing bearer token")

    token = creds.credentials
    verify_azure_jwt(token)
    return
