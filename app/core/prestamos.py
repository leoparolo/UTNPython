from datetime import date, timedelta
from app.core.database import SessionLocal
from app.models.prestamos import Prestamo
from app.models.usuarios import Usuario
from app.models.libros import Libro

class GestorPrestamos:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self, estado: str | None = None, usuario_id: int | None = None,
                  libro_id: int | None = None, page: int = 1, size: int = 20):
        q = self.session.query(Prestamo)
        if estado:
            q = q.filter(Prestamo.estado == estado)
        if usuario_id:
            q = q.filter(Prestamo.usuario_id == usuario_id)
        if libro_id:
            q = q.filter(Prestamo.libro_id == libro_id)
        return q.order_by(Prestamo.prestamo_id.desc()).offset((page-1)*size).limit(size).all()

    def get_por_id(self, prestamo_id: int):
        return self.session.query(Prestamo).get(prestamo_id)

    def crear(self, usuario_id: int, libro_id: int):
        usuario = self.session.query(Usuario).get(usuario_id)
        libro = self.session.query(Libro).get(libro_id)

        if not usuario or not libro:
            return None, "Usuario o Libro inexistente"

        if not usuario.estado or (usuario.estado.nombre or "").lower() != "activo":
            return None, "Usuario no habilitado para préstamos"

        if (libro.ejemplares_disponibles or 0) <= 0:
            return None, "No hay ejemplares disponibles de este libro"

        duplicado = (
            self.session.query(Prestamo)
            .filter(
                Prestamo.usuario_id == usuario_id,
                Prestamo.libro_id == libro_id,
                Prestamo.estado != "devuelto",
            )
            .first()
        )
        if duplicado:
            return None, "Ya existe un préstamo pendiente de este libro para el usuario"

        dias = 7
        if usuario.rol and usuario.rol.dias_prestamos:
            dias = usuario.rol.dias_prestamos

        hoy = date.today()
        nuevo = Prestamo(
            usuario_id=usuario_id,
            libro_id=libro_id,
            fecha_prestamo=hoy,
            fecha_devolucion_esperada=hoy + timedelta(days=dias),
            estado="pendiente",
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
        prestamo = self.session.query(Prestamo).get(prestamo_id)
        if not prestamo:
            return None, "Préstamo no encontrado"
        if prestamo.estado == "devuelto":
            return None, "El préstamo ya fue devuelto"
        try:
            prestamo.estado = "devuelto"
            libro = self.session.query(Libro).get(prestamo.libro_id)
            if libro:
                libro.ejemplares_disponibles = (libro.ejemplares_disponibles or 0) + 1
            self.session.commit()
            self.session.refresh(prestamo)
            return prestamo, None
        except Exception as e:
            self.session.rollback()
            print(f"Error devolver préstamo: {e}")
            return None, "No se pudo devolver el préstamo"

db_prestamos = GestorPrestamos()
