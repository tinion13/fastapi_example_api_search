import logging
from datetime import datetime

from pydantic import ValidationError

from clients.weathers import WeathersClient
from exceptions.weathers import (
    WeathersClientResponseError,
    WeathersClientTransportError,
    WeathersProviderUnavailable,
    WeathersServiceBadResponseError,
    WeathersServiceValidationError,
)
from schemas.weathers import ForecastOutputUser, WeathersNormalizedInput, WeathersOutputUser, WeathersProviderAnswer
from utils.common import format_ts_to_str
from utils.weathers import wind_direction_16

log = logging.getLogger(__file__)


class WeathersService:
    def __init__(
        self,
        client: WeathersClient,
    ) -> None:
        self._client = client

    async def get_forecasts(
        self,
        params: WeathersNormalizedInput
    ) -> WeathersOutputUser:
        try:
            response = await self._client.get_result(params)
        except WeathersClientTransportError as ex:
            raise WeathersProviderUnavailable(ex) from ex
        except WeathersClientResponseError as ex:
            raise WeathersServiceBadResponseError(ex) from ex

        try:
            answer = WeathersProviderAnswer.model_validate(response)
        except ValidationError as ex:
            raise WeathersServiceValidationError(ex) from ex

        forecasts_raw = answer.forecasts

        #FIXME: check if answer.forecasts[] have rain and/or snow
        for forecast in forecasts_raw:
            if forecast.rain or forecast.snow:
                log.warning(f"answer.forecasts[] have rain and/or snow: {forecast}")
                break

        try:
            output = WeathersOutputUser(
                city_name=answer.city.name,
                sunrise=format_ts_to_str(answer.city.sunrise, answer.city.timezone),
                sunset=format_ts_to_str(answer.city.sunset, answer.city.timezone),
                forecasts=[]
            )

            for forecast in forecasts_raw:
                output.forecasts.append(
                    ForecastOutputUser(
                        date=datetime.fromisoformat(forecast.dt_txt).strftime("%Y.%m.%d %H:%M"),
                        temperature=forecast.main.temp,
                        feels_like=forecast.main.feels_like,
                        pressure=forecast.main.pressure,
                        humidity=forecast.main.humidity,
                        weather_description=forecast.weather[0].description,
                        cloudiness=forecast.clouds.all,
                        wind_speed=forecast.wind.speed,
                        wind_gust=forecast.wind.gust,
                        wind_direction=wind_direction_16(forecast.wind.deg),
                        visibility=forecast.visibility,
                        pop=forecast.pop,
                    )
                )
        except ValidationError as ex:
            raise WeathersServiceValidationError(ex) from ex

        return output
