from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.core.error import AppException

def register_error_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(request),
            media_type="application/problem+json"
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "type": "about:blank",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "Ocurrió un error inesperado.",
                "instance": str(request.url),
            },
            media_type="application/problem+json"
        )
