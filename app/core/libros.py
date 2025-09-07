from app.core.database import SessionLocal
from app.models.libros import Libro

class GestorLibros:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, q: str | None = None, page: int = 1, size: int = 20):
        query = self.session.query(Libro)
        if q:
            query = query.filter(Libro.titulo.ilike(f"%{q}%"))
        return query.order_by(Libro.libro_id).offset((page-1)*size).limit(size).all()

    def get_por_id(self, libro_id: int):
        return self.session.query(Libro).get(libro_id)

    def crear(self, datos: dict):
        nuevo = Libro(**datos)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
            return nuevo
        except Exception as e:
            self.session.rollback()
            print(f"Error crear libro: {e}")
            raise

    def actualizar(self, libro_id: int, actualizacion: dict):
        libro = self.session.query(Libro).get(libro_id)
        if not libro:
            return None
        for campo, valor in actualizacion.items():
            setattr(libro, campo, valor)
        try:
            self.session.commit()
            self.session.refresh(libro)
            return libro
        except Exception as e:
            self.session.rollback()
            print(f"Error actualizar libro: {e}")
            raise

    def eliminar(self, libro_id: int):
        libro = self.session.query(Libro).get(libro_id)
        if not libro:
            return None
        try:
            self.session.delete(libro)
            self.session.commit()
            return libro
        except Exception as e:
            self.session.rollback()
            print(f"Error eliminar libro: {e}")
            raise

db_libros = GestorLibros()
