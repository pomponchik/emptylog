from typing import Any

try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]


@runtime_checkable
class LoggerProtocol(Protocol):
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: return None
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: return None
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: return None
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: return None
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: return None
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: return None


class LoggerMethodProtocol(Protocol):
    def __call__(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # pragma: no cover
