from app.core.database import SessionLocal
from app.models.ubicaciones import Ubicacion

class GestorUbicaciones:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Ubicacion).order_by(Ubicacion.ubicacion_id).all()
    
db = GestorUbicaciones()