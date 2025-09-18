from app.core.database import SessionLocal
from app.models.usuarios import Usuario

class GestorUsuarios:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Usuario).order_by(Usuario.usuario_id).all()

    def get_por_id(self,usuario_id: int):
        return self.session.query(Usuario).get(usuario_id)

    def crear(self,data: dict):
        nuevo = Usuario(**data)
        try:
            self.session.add(nuevo)
            self.session.commit()
            self.session.refresh(nuevo)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            raise
        return nuevo

    def actualizar(self,usuario_id: int, data: dict):
        usuario = self.session.query(Usuario).get(usuario_id)
        if not usuario:
            return None
        for key, value in data.items():
            setattr(usuario, key, value)
        try:
            self.session.commit()
            self.session.refresh(usuario)
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            raise
        return usuario

    def eliminar(self,usuario_id: int):
        usuario = self.session.query(Usuario).get(usuario_id)
        if not usuario:
            return None
        try:
            self.session.delete(usuario)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            raise
        return usuario

db = GestorUsuarios()
