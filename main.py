from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.autores import router as autores_router
from app.api.wikipedia import router as wikipedia_router
from app.api.libros import router as libros_router
from app.api.prestamos import router as prestamos_router
from app.api.usuarios import router as usuarios_router
from app.api.roles import router as roles_router
from app.api.estados_usuarios import router as estados_usuarios_router
from app.api.nacionalidades import router as nacionalidades_router

from app.frontend.autores import router as frontend_autores_router
from app.frontend.libros import router as frontend_libros_router
from app.frontend.prestamos import router as frontend_prestamos_router
from app.frontend.usuarios import router as frontend_usuarios_router

from app.models import Base
from app.core.database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Open Biblioteca API", version="1.0.0")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(autores_router, prefix="/api")
app.include_router(wikipedia_router, prefix="/api")
app.include_router(libros_router, prefix="/api")
app.include_router(prestamos_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(estados_usuarios_router, prefix="/api")
app.include_router(usuarios_router, prefix="/api")
app.include_router(nacionalidades_router, prefix="/api")

app.include_router(frontend_autores_router)
app.include_router(frontend_libros_router)
app.include_router(frontend_prestamos_router)
app.include_router(frontend_usuarios_router)
