from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def setup_error_handlers(app):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        context = {
            "request": request,
            "detail": exception.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "exc_type": "RequestValidationError"
        }
        return JSONResponse(
            context,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        context = {
            "request": request,
            "detail": str(exception),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "exc_type": "Exception"
        }
        return JSONResponse(
            context,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
