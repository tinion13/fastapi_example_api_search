from fastapi import Depends

from core.settings.secrets import Secrets, get_secrets
from modules.avia_tickets.client import AviaTicketsClient
from modules.shared.dependencies.client import get_base_api_client


async def get_avia_tickets_client(
    base_api_client = Depends(get_base_api_client),
    secrets: Secrets = Depends(get_secrets)
) -> AviaTicketsClient:
    return AviaTicketsClient(
        client=base_api_client,
        api_key=secrets.TRAVELPAYOUTS_AVIASALES_TOKEN.get_secret_value()
    )
