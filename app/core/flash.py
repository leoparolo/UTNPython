from fastapi import Request

FLASH_KEY = "flash_message"

def set_flash(request: Request, tipo: str, texto: str) -> None:
    """
    Guarda un mensaje flash en la sesión.
    - tipo: success | error | info | warning
    - texto: mensaje a mostrar
    """
    request.session[FLASH_KEY] = {"tipo": tipo, "texto": texto}

def get_flash(request: Request):
    """
    Recupera y elimina el mensaje flash de la sesión.
    Devuelve None si no había mensaje.
    """
    return request.session.pop(FLASH_KEY, None)
