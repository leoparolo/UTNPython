from fastapi import Request

class AppException(Exception):
    def __init__(
        self,
        title: str,
        detail: str,
        status_code: int = 400,
        type_: str = "about:blank",
    ):
        """
        Implementa RFC 7807 (application/problem+json).
        """
        self.title = title
        self.detail = detail
        self.status_code = status_code
        self.type = type_
        self.instance = None

    def to_dict(self, request: Request) -> dict:
        return {
            "type": self.type,
            "title": self.title,
            "status": self.status_code,
            "detail": self.detail,
            "instance": str(request.url),
        }
