from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WeathersSearchInput(BaseModel):
    city: str = Field(min_length=3)


class WeathersNormalizedInput(BaseModel):
    lat: float
    lon: float
    units: Literal["standard", "metric", "imperial"] = "metric"
    mode: Literal["json"] = "json"
    cnt: int | None = None
    lang: str = "ru"


class ForecastMainProviderAnswer(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: int
    grnd_level: int
    humidity: int
    temp_kf: float


class ForecastWeatherProviderAnswer(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class ForecastCloudsProviderAnswer(BaseModel):
    all: int


class ForecastWindProviderAnswer(BaseModel):
    speed: float
    deg: int
    gust: float


class ForecastSysProviderAnswer(BaseModel):
    pod: Literal["n", "d"]


class ForecastProviderAnswer(BaseModel):
    dt: int
    main: ForecastMainProviderAnswer
    weather: list[ForecastWeatherProviderAnswer]
    clouds: ForecastCloudsProviderAnswer
    wind: ForecastWindProviderAnswer
    visibility: int
    pop: float
    rain: dict | None = None
    snow: dict | None = None
    sys: ForecastSysProviderAnswer
    dt_txt: str


class CityCoordinatesProviderAnswer(BaseModel):
    lat: float
    lon: float


class CityProviderAnswer(BaseModel):
    id: int
    name: str
    coord: CityCoordinatesProviderAnswer
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class WeathersProviderAnswer(BaseModel):
    cod: str
    message: int
    cnt: int
    forecasts: list[ForecastProviderAnswer] = Field(alias="list")
    city: CityProviderAnswer

    model_config = ConfigDict(extra="ignore")


class ForecastOutputUser(BaseModel):
    date: str
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    weather_description: str
    cloudiness: int
    wind_speed: float
    wind_gust: float
    wind_direction: str
    visibility: int
    pop: float


class WeathersOutputUser(BaseModel):
    city_name: str
    sunrise: str
    sunset: str
    forecasts: list[ForecastOutputUser]
