from app.core.database import SessionLocal
from app.models.usuarios import Usuario

class GestorUsuarios:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Usuario).order_by(Usuario.usuario_id).all()
    
db = GestorUsuarios()