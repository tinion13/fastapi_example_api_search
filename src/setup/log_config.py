import atexit
import contextlib
import logging
from pathlib import Path

from core.paths import BASE_DIR


class FileRouterHandler(logging.Handler):
    def __init__(self, logs_root: Path) -> None:
        super().__init__()
        self.logs_root = logs_root
        self._handlers: dict[Path, logging.FileHandler] = {}

    def _path_for(self, logger_name: str) -> Path:
        parts = logger_name.split(".")
        *dirs, filename = parts
        return self.logs_root.joinpath(*dirs, f"{filename}.log")

    def _get_or_create_handler(self, path: Path) -> logging.FileHandler:
        handler = self._handlers.get(path)
        if handler is not None:
            return handler

        path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setLevel(logging.NOTSET)
        handler.setFormatter(self.formatter)
        self._handlers[path] = handler
        return handler

    def emit(self, record: logging.LogRecord) -> None:
        try:
            path = self._path_for(record.name)
            handler = self._get_or_create_handler(path)
            handler.emit(record)
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        for handler in self._handlers.values():
            with contextlib.suppress(Exception):
                handler.close()
        self._handlers.clear()
        super().close()


def setup_logging(level: str = "INFO", logs_dir: str | Path = "logs") -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    router = FileRouterHandler(BASE_DIR / logs_dir)
    router.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s : %(message)s")
    )
    root.addHandler(router)
    atexit.register(router.close)
