import logging

import structlog
from {{ __template_name }}.config import settings


def _configure_root_logger() -> None:
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    root_logger.setLevel(settings.LOG_LEVEL.upper())
    root_logger.addHandler(handler)


def _configure_global_structlog_defaults() -> None:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )


def _setup_logging() -> None:
    _configure_root_logger()
    _configure_global_structlog_defaults()


_setup_logging()
log = structlog.get_logger()
