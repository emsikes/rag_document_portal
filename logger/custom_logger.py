import logging
import os
from datetime import datetime
import structlog

class CustomLogger:
    """
    Customer logging class for the document_portal application
    """

    def __init__(self, log_dir="logs"):
        # Ensure log directory exists
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Create timestampted log file name
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H.%M.%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    def get_logger(self, name =__file__):
        logger_name = os.path.basename(name)

        # Configure logging for console and file output in JSON format
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s", # Structlog will handle JSON format rendering
            handlers=[console_handler, file_handler]
        )

        # Configure structlog foor JSON structured logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.getLogger(logger_name)
    

if __name__ == "__main__":
    logger = CustomLogger()
    logger = logger.get_logger(__file__)
    logger.info("Custom logger initialized.")