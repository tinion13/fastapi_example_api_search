from fastapi import APIRouter

from routers.avia_tickets import router as avia_tickets
from routers.home import router as home_page

router = APIRouter()

router.include_router(home_page, tags=["home_page"])
router.include_router(avia_tickets, tags=["avia_tickets"])
