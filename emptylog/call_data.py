from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass
class LoggerCallData:
    message: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
