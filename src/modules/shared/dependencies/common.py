from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.reference_data.data_loader import Data


async def get_templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates


async def get_data(request: Request) -> Data:
    return request.app.state.data
