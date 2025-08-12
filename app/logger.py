import logging.config
import json

def get_logger(config_path: str = "logger_conf.json") -> logging.Logger:
    with open(config_path, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)
