import logging
from datetime import datetime

from pydantic import ValidationError

from clients.avia_tickets import AviaTicketsClient
from data.data_loader import Data
from exceptions.avia_tickets import (
    AviaTicketsClientResponseError,
    AviaTicketsClientTransportError,
    AviaTicketsProviderUnavailable,
    AviaTicketsServiceBadResponseError,
    AviaTicketsServiceValidationError,
)
from schemas.avia_tickets import AviaTicketsProviderAnswer, AviaTicketsSearchInput, Flight

log = logging.getLogger(__file__)


class AviaTicketsService:
    def __init__(
        self,
        client: AviaTicketsClient,
        data: Data
    ) -> None:
        self._client = client
        self._data = data

    async def get_flights(
        self,
        params: AviaTicketsSearchInput
    ) -> list[Flight]:
        try:
            response = await self._client.get_result(params)
        except AviaTicketsClientTransportError as ex:
            raise AviaTicketsProviderUnavailable(ex) from ex
        except AviaTicketsClientResponseError as ex:
            raise AviaTicketsServiceBadResponseError(ex) from ex

        try:
            answer = AviaTicketsProviderAnswer.model_validate(response)
        except ValidationError as ex:
            raise AviaTicketsServiceValidationError(ex) from ex

        flights = answer.data
        for flight in flights:
            flight.price = f"{flight.price} RUB"
            flight.link = f"https://www.aviasales.ru{flight.link}"
            flight.airline = self._data.aircompanies.get(flight.airline, flight.airline)
            flight.departure_at = datetime.fromisoformat(flight.departure_at).strftime("%Y.%m.%d %H:%M")
            flight.return_at = datetime.fromisoformat(flight.return_at).strftime("%Y.%m.%d %H:%M")

        return flights
