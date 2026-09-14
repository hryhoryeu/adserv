import json
from datetime import UTC, datetime
from logging import Filter, Formatter, LogRecord
from logging.config import dictConfig

from app.core.context_variables import request_id_var

STANDARD = set(LogRecord("", 0, "", 0, {}, None, None).__dict__) | {
    "message",
    "asctime",
}


class ContextFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class JSONFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        result = {
            "ts": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": record.request_id,
        }
        result.update({k: v for k, v in record.__dict__.items() if k not in STANDARD})
        if exc_info := record.exc_info:
            result["exc"] = self.formatException(exc_info)
        return json.dumps(result, default=str)


def setup_logging(level: str = "INFO", format: str = "console") -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "context": {"()": "app.core.logger.ContextFilter"},
            },
            "formatters": {
                "json": {"()": "app.core.logger.JSONFormatter"},
                "console": {
                    "format": "%(asctime)s %(levelname)-7s [%(request_id)-36s] %(name)s: %(msg)s"
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": format,
                    "filters": ["context"],
                },
            },
            "root": {"level": level, "handlers": ["console"]},
            "loggers": {
                # uvicorn по умолчанию ставит свои хэндлеры — забираем его в root
                "uvicorn": {"handlers": [], "propagate": True},
                "uvicorn.error": {"handlers": [], "propagate": True},
                "uvicorn.access": {
                    "handlers": [],
                    "propagate": True,
                    "level": "WARNING",
                },
                # шумные библиотеки
                "httpx": {"level": "WARNING"},
            },
        }
    )
