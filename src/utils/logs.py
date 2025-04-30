import logging
import sys
from typing import Optional

class Logger:
    """
    A reusable and configurable logger instance.
    """

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        log_to_file: bool = False,
        filename: Optional[str] = "app.log"
    ):
        """
        Initializes the logger.

        Args:
            name (str): Logger name.
            level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
            log_to_file (bool): Whether to write logs to a file.
            filename (Optional[str]): File path for the log file.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Avoid duplicate handlers
        if not self.logger.handlers:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            if log_to_file and filename:
                file_handler = logging.FileHandler(filename)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger
