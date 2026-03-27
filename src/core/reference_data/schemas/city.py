from pydantic import BaseModel, TypeAdapter


class Coordinates(BaseModel):
    lat: float
    lon: float


class CityCodeCoordinates(BaseModel):
    code: str
    coordinates: Coordinates


cities_adapter = TypeAdapter(dict[str, CityCodeCoordinates])
