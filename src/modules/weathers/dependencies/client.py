from fastapi import Depends

from core.settings.secrets import Secrets, get_secrets
from modules.shared.dependencies.client import get_base_api_client
from modules.weathers.client import WeathersClient


async def get_weathers_client(
    base_api_client = Depends(get_base_api_client),
    secrets: Secrets = Depends(get_secrets)
) -> WeathersClient:
    return WeathersClient(
        client=base_api_client,
        api_key=secrets.OPENWEATHER_TOKEN.get_secret_value()
    )
