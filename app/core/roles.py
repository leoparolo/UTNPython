from app.core.database import SessionLocal
from app.models.roles import Rol

class GestorRoles:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Rol).order_by(Rol.rol_id).all()

db = GestorRoles()
