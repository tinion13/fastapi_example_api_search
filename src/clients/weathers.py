import json
import logging

import httpx

from clients.base import BaseApiClient
from exceptions.weathers import WeathersClientResponseError, WeathersClientTransportError
from schemas.weathers import WeathersSearchInput

log = logging.getLogger(__file__)

class WeathersClient(BaseApiClient):
    async def get_result(
        self,
        params: WeathersSearchInput,
    ) -> dict:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        headers = {'Accept-Encoding': 'gzip, deflate'}
        params_provider = params.model_dump(exclude_none=True)
        params_provider["appid"] = self._api_key

        try:
            response = await self._client.get(url, params=params_provider, headers=headers)
            response.raise_for_status()
            response = response.json()
        except httpx.HTTPStatusError as ex:
            raise WeathersClientResponseError(ex) from ex
        except httpx.HTTPError as ex:
            raise WeathersClientTransportError(ex) from ex
        except json.JSONDecodeError as ex:
            raise WeathersClientResponseError(ex) from ex

        return response
