from typing import Any

try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]


@runtime_checkable
class LoggerProtocol(Protocol):
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: pass
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: pass
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: pass
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: pass
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: pass
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: pass
