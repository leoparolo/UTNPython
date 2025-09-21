from datetime import date, timedelta
from app.core.database import SessionLocal
from app.models.prestamos import Prestamo
from app.models.usuarios import Usuario
from app.models.libros import Libro
from app.schemas.prestamos import PrestamoCreate

class GestorPrestamos:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Prestamo).order_by(Prestamo.prestamo_id).all()

    def get_por_id(self, prestamo_id: int):
        return self.session.query(Prestamo).get(prestamo_id)

    def crear(self, datos_prestamo:dict):
        nuevo = PrestamoCreate(**datos_prestamo)
        usuario = self.session.query(Usuario).get(nuevo.usuario_id)
        libro = self.session.query(Libro).get(nuevo.libro_id)

        if not usuario or not libro:
            return None, "Usuario o Libro inexistente"

        if not usuario.estado or (usuario.estado.nombre or "").lower() != "activo":
            return None, "Usuario no habilitado para préstamos"

        if (libro.ejemplares_disponibles or 0) <= 0:
            return None, "No hay ejemplares disponibles de este libro"

        duplicado = (
            self.session.query(Prestamo)
            .filter(
                Prestamo.usuario_id == nuevo.usuario_id,
                Prestamo.libro_id == nuevo.libro_id,
                Prestamo.estado != "devuelto",
            )
            .first()
        )
        if duplicado:
            return None, "Ya existe un préstamo pendiente de este libro para el usuario"

        dias = 7
        if usuario.rol and usuario.rol.dias_prestamo:
            dias = usuario.rol.dias_prestamo

        hoy = date.today()
        nuevo = Prestamo(
            usuario_id=nuevo.usuario_id,
            libro_id=nuevo.libro_id,
            fecha_prestamo=hoy,
            fecha_devolucion_esperada=hoy + timedelta(days=dias),
            estado="activo",
        )
        try:
            libro.ejemplares_disponibles = (libro.ejemplares_disponibles or 0) - 1
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
            return nuevo, None
        except Exception as e:
            self.session.rollback()
            print(f"Error crear préstamo: {e}")
            return None, "No se pudo crear el préstamo"

    def devolver(self, prestamo_id: int):
        prestamo = self.session.get(Prestamo, prestamo_id)
        if not prestamo:
            return None, "Préstamo no encontrado"
        try:
            prestamo.estado = "completado"
            prestamo.fecha_devolucion_real = date.today()
            libro = self.session.get(Libro, prestamo.libro_id)
            if libro:
                libro.ejemplares_disponibles = (libro.ejemplares_disponibles or 0) + 1
            self.session.commit()
            self.session.refresh(prestamo)
            return prestamo, None
        except Exception as e:
            self.session.rollback()
            print(f"Error devolver préstamo: {e}")
            return None, "No se pudo devolver el préstamo"

db = GestorPrestamos()
