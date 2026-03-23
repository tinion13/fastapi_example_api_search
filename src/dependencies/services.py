from fastapi import Depends

from clients.avia_tickets import AviaTicketsClient
from data.data_loader import Data
from dependencies.clients import get_avia_tickets_client
from dependencies.common import get_data
from services.avia_tickets import AviaTicketsService


async def get_avia_tickets_service(
    client: AviaTicketsClient = Depends(get_avia_tickets_client),
    data: Data = Depends(get_data),
) -> AviaTicketsService:
    return AviaTicketsService(
        client=client,
        data=data,
    )
