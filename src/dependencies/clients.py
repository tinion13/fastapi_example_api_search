import httpx
from fastapi import Depends, Request

from clients.avia_tickets import AviaTicketsClient
from core.settings import Settings, get_settings


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


async def get_avia_tickets_client(
    http_client = Depends(get_http_client),
    settings: Settings = Depends(get_settings)
) -> AviaTicketsClient:
    return AviaTicketsClient(
        client=http_client,
        api_key=settings.TRAVELPAYOUTS_AVIASALES_TOKEN.get_secret_value()
    )
