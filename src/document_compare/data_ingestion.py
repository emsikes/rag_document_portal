import sys
from pathlib import Path
import fitz

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocoumentCompare:
    def __init__(self):
        pass

    def delete_existing_file(self):
        """
        Delete existing files in the specified path
        """
        pass

    def save_uploaded_files(self):
        """
        Save uploaded files in the specified directory
        """
        pass

    def read_pdf(self):
        """
        Reads a PDF file and extracts text from each page
        """
        pass

