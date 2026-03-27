from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.paths import STATIC_DIR, TEMPLATES_DIR
from core.reference_data.data_loader import load_data
from core.settings.app_config import AppConfig
from setup.errors_pages import setup_error_handlers
from setup.log_config import setup_logging
from setup.routes import router as root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_cfg = AppConfig.from_sources()
    setup_logging(app_cfg.logging.level)

    app.state.api_client = httpx.AsyncClient(timeout=10)
    app.state.templates = Jinja2Templates(directory=TEMPLATES_DIR)
    app.state.data = load_data()
    yield
    await app.state.api_client.aclose()


app = FastAPI(lifespan=lifespan, title="API Search")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
setup_error_handlers(app)
app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
