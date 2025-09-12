from app.core.database import SessionLocal
from app.models.categorias import Categoria

class GestorCategorias:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Categoria).order_by(Categoria.categoria_id).all()


db = GestorCategorias()