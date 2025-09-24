import httpx
from app.core.config import settings
from app.frontend.result import Result
from app.core.logging_config import logger


async def get() -> Result:
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.get("/autores/")
        if response.status_code != 200:
            error_msg = response.json().get("detail", "No detail in API response")
            logger.exception("Error al obtener autores: %s", error_msg)
            return Result(success=False, error="Error al obtener autores")
        return Result(success=True, data=response.json())

async def get_one(autor_id) -> Result:
    async with httpx.AsyncClient(base_url=settings.API_BASE_URL) as client:
        response = await client.get("/autores/{autor_id}")
        if response.status_code != 200:
            error_msg = response.json().get("detail", "No detail in API response")
            logger.exception("Error al obtener autor %s: %s",autor_id, error_msg)
            return Result(success=False, error="Error al obtener autor")
        return Result(success=True, data=response.json())
