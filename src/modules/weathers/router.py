import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from modules.weathers.dependencies.normalizer import get_weathers_normalized
from modules.weathers.dependencies.service import get_weathers_service
from modules.weathers.exceptions import (
    WeathersProviderUnavailable,
    WeathersServiceBadResponseError,
    WeathersServiceValidationError,
)
from modules.weathers.schemas import WeathersNormalizedInput
from modules.weathers.service import WeathersService

log = logging.getLogger(__file__)
router = APIRouter()


@router.post("/api/weathers")
async def get_forecasts(
    _: Request,
    params: WeathersNormalizedInput = Depends(get_weathers_normalized),
    weathers_service: WeathersService = Depends(get_weathers_service),
):
    log.debug(params)
    try:
        result = await weathers_service.get_forecasts(params)
    except WeathersProviderUnavailable as ex:
        log.exception("WeathersProviderUnavailable")
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Provider unavailable") from ex
    except WeathersServiceBadResponseError as ex:
        log.exception("WeathersServiceBadResponseError")
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Bad provider response") from ex
    except WeathersServiceValidationError as ex:
        log.exception("WeathersServiceValidationError")
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Bad provider answer") from ex

    return JSONResponse(
        {"data": result.model_dump()},
        status.HTTP_200_OK
    )
