from app.core.database import SessionLocal
from app.models.editoriales import Editorial

class GestorEditoriales:
    def __init__(self):
        self.session = SessionLocal()

    def get_todos(self):
        return self.session.query(Editorial).order_by(Editorial.editorial_id).all()
    
db = GestorEditoriales()