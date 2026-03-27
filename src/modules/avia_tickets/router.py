import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from modules.avia_tickets.dependencies.normalizer import get_avia_tickets_normalized
from modules.avia_tickets.dependencies.service import get_avia_tickets_service
from modules.avia_tickets.exceptions import (
    AviaTicketsProviderUnavailable,
    AviaTicketsServiceBadResponseError,
    AviaTicketsServiceValidationError,
)
from modules.avia_tickets.schemas import AviaTicketsSearchInput, list_flights_adapter
from modules.avia_tickets.service import AviaTicketsService

log = logging.getLogger(__file__)
router = APIRouter()


@router.post("/api/avia_tickets")
async def get_flights(
    _: Request,
    params: AviaTicketsSearchInput = Depends(get_avia_tickets_normalized),
    avia_tickets_service: AviaTicketsService = Depends(get_avia_tickets_service),
):
    log.debug(params)
    try:
        result = await avia_tickets_service.get_flights(params)
    except AviaTicketsProviderUnavailable as ex:
        log.exception("AviaTicketsProviderUnavailable")
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Provider unavailable") from ex
    except AviaTicketsServiceBadResponseError as ex:
        log.exception("AviaTicketsServiceBadResponseError")
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Bad provider response") from ex
    except AviaTicketsServiceValidationError as ex:
        log.exception("AviaTicketsServiceValidationError")
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Bad provider answer") from ex

    return JSONResponse(
        {"data": list_flights_adapter.dump_json(result)},
        status.HTTP_200_OK
    )
