from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Result:
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None