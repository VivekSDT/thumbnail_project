import logging

def get_logger(name):
    """Logger configuration setup"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler("logs/process.log", mode="a")
        console_handler = logging.StreamHandler()

        fmt = logging.Formatter(
            "%(asctime)s [%(processName)s] [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        file_handler.setFormatter(fmt)
        console_handler.setFormatter(fmt)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger
