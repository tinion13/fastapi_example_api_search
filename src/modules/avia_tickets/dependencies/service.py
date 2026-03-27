from fastapi import Depends

from core.reference_data.data_loader import Data
from modules.avia_tickets.client import AviaTicketsClient
from modules.avia_tickets.dependencies.client import get_avia_tickets_client
from modules.avia_tickets.service import AviaTicketsService
from modules.shared.dependencies.common import get_data


async def get_avia_tickets_service(
    client: AviaTicketsClient = Depends(get_avia_tickets_client),
    data: Data = Depends(get_data),
) -> AviaTicketsService:
    return AviaTicketsService(
        client=client,
        data=data,
    )
