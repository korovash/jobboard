# app/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os
from .config import settings

def setup_logging():
    log_file = settings.LOG_FILE
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # make sure directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception:
            pass

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Formatter
    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

    # Console handler (useful during development)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Rotating file handler
    fh = RotatingFileHandler(
        filename=log_file,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    fh.setLevel(log_level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # reduce noisy libraries if desired
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn").setLevel(logging.INFO)

    access_log_file = os.path.join(os.path.dirname(settings.LOG_FILE), "access.log")

    access_handler = RotatingFileHandler(
        access_log_file,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    access_handler.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(message)s"))
    access_handler.setLevel(logging.INFO)

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers.clear()
    uvicorn_access_logger.addHandler(access_handler)
    uvicorn_access_logger.setLevel(logging.INFO)
    uvicorn_access_logger.propagate = False