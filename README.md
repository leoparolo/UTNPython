## 🔧 Instrucciones de Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/leoparolo/UTNPython.git
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate
```

En Linux / MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Levantar el servidor
```bash
uvicorn main:app --reload
```

### 5. Acceder a la aplicación
- **Swagger UI (API interactiva):**  
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc (documentación alternativa):**  
  [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Frontend HTML (formularios y vistas):**  
  [http://127.0.0.1:8000/autores](http://127.0.0.1:8000/autores)
