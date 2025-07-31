import logging
import os
from datetime import datetime

class CustomLogger:
    """
    Customer logging class for the document_portal application
    """

    def __init__(self):
        # Ensure log directory exists
        self.logs_dir = os.path.join(os.getcwd(),"logs")
        os.makedirs(self.logs_dir, exist_ok=True)

        # Create timestampted log file name
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H.%M.%S')}.log"
        log_file_path = os.path.join(self.logs_dir, log_file)

        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            filemode='a',
            format="[%(asctime)s] - %(levelname)s %(name)s - (line:%(lineno)d) - %(message)s",
            level=logging.INFO,
        )

    def get_logger(self, name =__file__):
        return logging.getLogger(os.path.basename(name))
    

if __name__ == "__main__":
    logger = CustomLogger()
    logger = logger.get_logger(__file__)
    logger.info("Custom logger initialized.")