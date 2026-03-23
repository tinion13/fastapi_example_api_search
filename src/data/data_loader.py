from pathlib import Path

from pydantic import BaseModel

from core.paths import DATA_DIR
from data.schemas.avia_tickets.aircompany import aircompanies_adapter
from data.schemas.avia_tickets.city import City, cities_adapter


class Data(BaseModel):
    at_aircompanies: dict[str, str]
    at_cities: list[City]


def read_json(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_data() -> Data:
    return Data(
        at_aircompanies=aircompanies_adapter.validate_json(read_json(DATA_DIR / "at_aircompanies.json")),
        at_cities=cities_adapter.validate_json(read_json(DATA_DIR / "at_cities.json")),
    )
