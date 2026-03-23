from pydantic import BaseModel, TypeAdapter


class NameTranslations(BaseModel):
    en: str


class Coordinates(BaseModel):
    lat: float
    lon: float


class Airport(BaseModel):
    name_translations: NameTranslations
    city_code: str
    country_code: str
    time_zone: str
    code: str
    iata_type: str
    name: str | None
    coordinates: Coordinates
    flightable: bool


airports_adapter = TypeAdapter(list[Airport])
