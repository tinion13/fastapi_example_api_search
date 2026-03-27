from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from core.reference_data.data_loader import Data
from modules.avia_tickets.schemas import AviaTicketsSearchInput
from modules.shared.dependencies.common import get_data


async def get_avia_tickets_normalized(
    params: AviaTicketsSearchInput,
    data: Data = Depends(get_data)
) -> AviaTicketsSearchInput:
    if not params.origin and not params.destination:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Необходимо указать город отправления и/или прибытия",
        )

    async def translate_name_to_IATA(city_name: str) -> str | None:
        if city_name in data.cities:
            return data.cities[city_name].code
        return None

    if params.origin:
        iata_name = await translate_name_to_IATA(params.origin)
        if not iata_name:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "Нет IATA кода для такого города",
            )
        params.origin = iata_name
        if not params.destination:
            params.unique = "true"

    if params.destination:
        iata_name = await translate_name_to_IATA(params.destination)
        if not iata_name:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "Нет IATA кода для такого города",
            )
        params.destination = iata_name

    return params
