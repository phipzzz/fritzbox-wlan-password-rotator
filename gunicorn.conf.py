from app.config import (
    DEBUG,
    GUNICORN_PORT
)

bind = f"0.0.0.0:{GUNICORN_PORT}"
workers = 1

loglevel = 'debug' if DEBUG else 'info'
level = "DEBUG" if DEBUG else "INFO"

errorlog = '-'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(r)s %(s)s %(b)s "%(f)s" "%(a)s"'

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s : %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "level": level,
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": level,
            "handlers": ["console"],
            "propagate": False,
        },
    },
    "root": {
        "level": level,
        "handlers": ["console"],
    },
}