import sys
import traceback
from logger.custom_logger import CustomLogger


logger = CustomLogger().get_logger(__file__)


class DocumentPortalException(Exception):
    """
    Customer exception for Document Portal Application
    """
    def __init__(self, error_message, error_detail:sys):
        # Capture the traceback 
        _,_,exc_tb = error_detail.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename # Fetch the filename where the error occurred
        self.lineno = exc_tb.tb_lineno # Fetch the line number in the file where the error occurred
        self.error_message = str(error_message) 
        self.traceback_str = ''.join(traceback.format_exception(*error_detail.exc_info())) # Capture full traceback details
    def __str__(self):
        return f"""
            Error in [{self.file_name}] at line [{self.lineno}]
            Message: {self.error_message}
            {self.traceback_str}
        """

if __name__ == "__main__":
    try:
        a = 1 / 0 # simulate a zero division exception
    except Exception as e:
        app_exc = DocumentPortalException(e,sys)
        logger.error(app_exc)

        raise app_exc