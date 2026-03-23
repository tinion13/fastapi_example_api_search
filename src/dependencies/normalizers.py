from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from data.data_loader import Data
from dependencies.common import get_data
from schemas.avia_tickets import AviaTicketsSearchInput


async def get_avia_tickets_normalized(
    params: AviaTicketsSearchInput,
    data: Data = Depends(get_data)
) -> AviaTicketsSearchInput:
    if not params.origin and not params.destination:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Необходимо указать город отправления и/или прибытия",
        )

    async def translate_name_to_IATA(name: str) -> str | None:
        for city in data.at_cities:
            if name in city.cases.values():
                return city.code
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
