import httpx
from fastapi import Request


async def get_base_api_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.api_client
