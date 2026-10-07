import logging
from pathlib import Path


def setup_logger(log_file: str = "logs/app.log") -> logging.Logger:
    """Configure file and console logging."""
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("student_info_system")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
