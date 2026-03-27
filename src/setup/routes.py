from fastapi import APIRouter

from modules.avia_tickets.router import router as avia_tickets
from modules.shared.router import router as home_page

router = APIRouter()

router.include_router(home_page, tags=["home_page"])
router.include_router(avia_tickets, tags=["avia_tickets"])
