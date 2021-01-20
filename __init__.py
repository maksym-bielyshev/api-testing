import logging.config
from config import LOG_FILE

logging_settings = {
    "version": 1,
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s - %(name)s - %(funcName)s - %(message)s"
        },
    },
    "handlers": {
        "client": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": LOG_FILE
        },
        "conftest": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": LOG_FILE
        },
    },
    "loggers": {
        "client": {
            "handlers": ["client"],
            "level": "INFO"
        },
        "conftest": {
            "handlers": ["conftest"],
            "level": "INFO"
        },
    },
}

logging.config.dictConfig(logging_settings)
