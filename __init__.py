import logging.config

logging_settings = {
    "version": 1,
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "client": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": "info.log"
        },
        "conftest": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": "info.log"
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
