from dataclasses import dataclass
from typing import Tuple, Dict, Any


@dataclass
class LoggerCallData:
    message: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
