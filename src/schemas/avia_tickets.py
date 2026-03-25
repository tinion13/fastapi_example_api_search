from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from schemas.base import DefisYearMonthOrDateOrNone


class AviaTicketsSearchInput(BaseModel):
    currency: str = "RUB"
    origin: str | None = None
    destination: str | None = None
    departure_at: DefisYearMonthOrDateOrNone | None = None
    return_at: DefisYearMonthOrDateOrNone | None = None
    one_way: Literal["false"] = "false"
    direct: Literal["true", "false"] = "false"
    market: str = "ru"
    limit: int = 30
    page: int = 1
    sorting: Literal["price", "route"] = "price"
    unique: Literal["true", "false"] = "false"


class Flight(BaseModel):
    origin: str
    destination: str
    origin_airport: str
    destination_airport: str
    price: str
    airline: str
    flight_number: int
    departure_at: str
    return_at: str
    transfers: int
    return_transfers: int
    duration: int
    duration_to: int
    duration_back: int
    link: str
    gate: str | None = None

    model_config = ConfigDict(extra="ignore")


list_flights_adapter = TypeAdapter(list[Flight])


class AviaTicketsProviderAnswer(BaseModel):
    success: bool
    data: list[Flight] = Field(default_factory=list)
    error: str | None = None
