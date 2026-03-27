import json

import httpx

from modules.avia_tickets.exceptions import AviaTicketsClientResponseError, AviaTicketsClientTransportError
from modules.avia_tickets.schemas import AviaTicketsSearchInput
from modules.shared.client import BaseApiClient


class AviaTicketsClient(BaseApiClient):
    async def get_result(
        self,
        params: AviaTicketsSearchInput,
    ) -> dict:
        url = "http://api.travelpayouts.com/aviasales/v3/prices_for_dates"
        headers = {'Accept-Encoding': 'gzip, deflate'}
        params_provider = params.model_dump(exclude_none=True)
        params_provider["token"] = self._api_key

        try:
            response = await self._client.get(url, params=params_provider, headers=headers)
            response.raise_for_status()
            response = response.json()
        except httpx.HTTPStatusError as ex:
            raise AviaTicketsClientResponseError(ex) from ex
        except httpx.HTTPError as ex:
            raise AviaTicketsClientTransportError(ex) from ex
        except json.JSONDecodeError as ex:
            raise AviaTicketsClientResponseError(ex) from ex

        return response
