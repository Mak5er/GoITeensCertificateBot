import logging
import logging.config
import sys


def setup_loggers() -> logging.Logger:
    root = logging.root
    root.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(
        'runtime.log',
        mode='w',
        encoding='utf-8'
    )

    stdout_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    stdout_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    stdout_handler.setFormatter(stdout_formatter)
    file_handler.setFormatter(file_formatter)

    root.addHandler(stdout_handler)
    root.addHandler(file_handler)

    return root


def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(logging.root.name).getChild(module_name)
    return logger
