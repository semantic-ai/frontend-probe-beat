from azure_ad_verify_token import verify_jwt
from .msal import MSALConfig


def verify_azure_jwt(token):
    config = MSALConfig()

    azure_ad_app_id = config.client_id
    azure_ad_issuer = config.issuer
    azure_ad_jwks_uri = "https://login.microsoftonline.com/common/discovery/keys"
    payload = verify_jwt(
        token=token,
        valid_audiences=[azure_ad_app_id],
        issuer=azure_ad_issuer,
        jwks_uri=azure_ad_jwks_uri,
        verify=False,
    )
    return payload
