from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from core.reference_data.data_loader import Data
from modules.shared.dependencies.common import get_data
from modules.weathers.schemas import WeathersNormalizedInput, WeathersSearchInput


async def get_weathers_normalized(
    params: WeathersSearchInput,
    data: Data = Depends(get_data)
) -> WeathersNormalizedInput:
    if params.city not in data.cities:
        raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "Нет информации по такому городу",
            )
    coordinates = data.cities[params.city].coordinates
    return WeathersNormalizedInput(
        lat=coordinates.lat,
        lon=coordinates.lon,
    )
