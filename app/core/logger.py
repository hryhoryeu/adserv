import json
import logging
from datetime import UTC, datetime
from logging import Filter, Formatter

from app.core.middleware.request_id import request_id_var


class ContextFilter(Filter):
    def filter(self, record):
        record.request_id = request_id_var.get()
        return record


class JSONFormatter(Formatter):
    def format(self, record):
        result = {
            "ts": str(datetime.fromtimestamp(record.created, tz=UTC)),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.msg,
            "request_id": record.request_id,
        }
        return json.dumps(result)


def setup_logging(level: str = "INFO", format: str = "plain") -> None:
    logging.config.dictConfig(
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
