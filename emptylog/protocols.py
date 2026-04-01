from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LoggerProtocol(Protocol):
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002


class LoggerMethodProtocol(Protocol):
    def __call__(self, message: str, *args: Any, **kwargs: Any) -> None: return None  # noqa: ARG002  # pragma: no cover
