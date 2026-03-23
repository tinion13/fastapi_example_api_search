from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dependencies.common import get_templates
from routers.avia_tickets import router as avia_tickets_router

router = APIRouter()
router.include_router(avia_tickets_router, tags=["avia_tickets"])


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    return templates.TemplateResponse("index.html", {"request": request, })
