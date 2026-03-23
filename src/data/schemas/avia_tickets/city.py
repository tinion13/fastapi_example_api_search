from pydantic import BaseModel, TypeAdapter


class NameTranslations(BaseModel):
    en: str

class Coordinates(BaseModel):
    lat: float
    lon: float


class City(BaseModel):
    name_translations: NameTranslations
    cases: dict[str, str]
    country_code: str
    code: str
    time_zone: str
    name: str | None
    coordinates: Coordinates
    has_flightable_airport: bool


cities_adapter = TypeAdapter(list[City])
