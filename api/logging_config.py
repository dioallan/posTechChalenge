# logging_config.py
import logging
from pythonjsonlogger import jsonlogger


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Handler para o console (stdout)
    console_handler = logging.StreamHandler()
    console_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo
    file_handler = logging.FileHandler('logsExecucao.json')
    file_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
