from fastapi import Depends

from modules.weathers.client import WeathersClient
from modules.weathers.dependencies.client import get_weathers_client
from modules.weathers.service import WeathersService


async def get_weathers_service(
    client: WeathersClient = Depends(get_weathers_client),
) -> WeathersService:
    return WeathersService(
        client=client,
    )
