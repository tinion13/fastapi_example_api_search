from pydantic import ValidationError

from core.reference_data.data_loader import Data
from modules.avia_tickets.client import AviaTicketsClient
from modules.avia_tickets.exceptions import (
    AviaTicketsClientResponseError,
    AviaTicketsClientTransportError,
    AviaTicketsProviderUnavailable,
    AviaTicketsServiceBadResponseError,
    AviaTicketsServiceValidationError,
)
from modules.avia_tickets.schemas import AviaTicketsProviderAnswer, AviaTicketsSearchInput, Flight
from modules.shared.utils.common import format_iso_to_str


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
            flight.departure_at = format_iso_to_str(flight.departure_at)
            flight.return_at = format_iso_to_str(flight.return_at)

        return flights
