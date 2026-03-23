import json
import logging

import httpx

from clients.base import BaseApiClient
from exceptions.avia_tickets import AviaTicketsClientResponseError, AviaTicketsClientTransportError
from schemas.avia_tickets import AviaTicketsSearchInput

log = logging.getLogger(__file__)

class AviaTicketsClient(BaseApiClient):
    async def get_result(
        self,
        params: AviaTicketsSearchInput,
    ) -> dict:
        url = 'http://api.travelpayouts.com/aviasales/v3/prices_for_dates'
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
