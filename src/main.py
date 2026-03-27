from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.errors_pages_setup import setup_error_handlers
from core.master_router import router as master_router
from core.paths import STATIC_DIR, TEMPLATES_DIR
from data.data_loader import load_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.api_client = httpx.AsyncClient(timeout=10)
    app.state.templates = Jinja2Templates(directory=TEMPLATES_DIR)
    app.state.data = load_data()
    yield
    await app.state.api_client.aclose()


app = FastAPI(lifespan=lifespan, title="Tickets Search")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
setup_error_handlers(app)
app.include_router(master_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
