import logging

# Configuración global
logging.basicConfig(
    level=logging.INFO,  # podés usar DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("errors.log", encoding="utf-8"),  # guarda en archivo
        logging.StreamHandler()  # sigue mostrando en consola
    ]
)

logger = logging.getLogger(__name__)
