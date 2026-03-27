from pathlib import Path

from pydantic import BaseModel

from core.paths import DATA_JSONS_DIR
from data.schemas.aircompany import aircompanies_adapter
from data.schemas.city import CityCodeCoordinates, cities_adapter


class Data(BaseModel):
    aircompanies: dict[str, str]
    cities: dict[str, CityCodeCoordinates]


def read_json(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_data() -> Data:
    return Data(
        aircompanies=aircompanies_adapter.validate_json(
            read_json(DATA_JSONS_DIR / "aircompanies.json")
        ),
        cities=cities_adapter.validate_json(
            read_json(DATA_JSONS_DIR / "cities_name_code_coordinates.json")
        ),
    )
