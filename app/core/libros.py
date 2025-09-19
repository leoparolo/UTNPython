from app.core.database import SessionLocal
from app.models.libros import Libro

class GestorLibros:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Libro).order_by(Libro.libro_id).all()

    def get_por_id(self, libro_id: int):
        return self.session.query(Libro).get(libro_id)

    def crear(self, datos: dict):
        if "ejemplares_disponibles" not in datos or datos["ejemplares_disponibles"] is None:
            datos["ejemplares_disponibles"] = datos.get("cantidad_ejemplares", 0)

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

        cantidad_ejemplares_db = libro.cantidad_ejemplares
        ejemplares_disponibles_db = libro.ejemplares_disponibles

        if "cantidad_ejemplares" in actualizacion:
            cantidad_ejemplares_new = actualizacion["cantidad_ejemplares"]

            prestados = cantidad_ejemplares_db - ejemplares_disponibles_db

            actualizacion["ejemplares_disponibles"] = max(0, cantidad_ejemplares_new - prestados)

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

db = GestorLibros()
