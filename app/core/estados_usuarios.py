from app.core.database import SessionLocal
from app.models.estados_usuarios import EstadoUsuario

class GestorEstadosUsuarios:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(EstadoUsuario).order_by(EstadoUsuario.estado_id).all()

db = GestorEstadosUsuarios()
