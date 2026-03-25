import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from dependencies.normalizers import get_weathers_normalized
from dependencies.services import get_weathers_service
from exceptions.weathers import (
    WeathersProviderUnavailable,
    WeathersServiceBadResponseError,
    WeathersServiceValidationError,
)
from schemas.weathers import WeathersNormalizedInput
from services.weathers import WeathersService

log = logging.getLogger(__file__)
router = APIRouter()


@router.post("/api/weathers")
async def get_forecast(
    _: Request,
    params: WeathersNormalizedInput = Depends(get_weathers_normalized),
    weathers_service: WeathersService = Depends(get_weathers_service),
):
    try:
        result = await weathers_service.get_forecasts(params)
    except WeathersProviderUnavailable as ex:
        log.exception(str(ex))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Provider unavailable") from ex
    except WeathersServiceBadResponseError as ex:
        log.exception(str(ex))
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Bad provider response") from ex
    except WeathersServiceValidationError as ex:
        log.exception(str(ex))
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Bad provider answer") from ex

    return JSONResponse(
        {"data": result.model_dump()},
        status.HTTP_200_OK
    )
