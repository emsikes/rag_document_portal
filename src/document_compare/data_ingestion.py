import sys
from pathlib import Path
import fitz

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocoumentIngestion:
    def __init__(self, base_dir: str = ".\\data\\document_compare"):
        self.log = CustomLogger.get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.bas_dir.mkdir(parents=True, exist_ok=True)

    def delete_existing_file(self):
        """
        Delete existing files in the specified path
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted", path=str(file))
                self.log.info("Directory cleaned", directory=str(self.base_dir))
        except Exception as e:
            self.log.error(f"Error deleteing existing files: {e}")
            raise DocumentPortalException("An error occorrued while deleting existing files.", sys)
                           
    def save_uploaded_files(self, reference_file, actual_file):
        """
        Save uploaded files in the specified directory.
        refernce_file is the first file, actual_file is the second file in our comparisin
        """
        try:
            self.delete_existing_file()
            self.log.info("Existing file deleted successfully.")

            # Join base dir and file name variables to get the full path
            reference_path = self.base_dir/ reference_file.name
            actual_path = self.base_dir/ actual_file.name

            if not reference_file.name.endswith(".pfd") or not actual_file.name.endswith(".pdf"):
                raise ValueError("only PF files are allowed.")
            
            with open(reference_path, "wb") as f:
                f.write(reference_file.getbuffer())

            with open(actual_path, "wb") as f:
                f.write(actual_file.get_buffer())

            self.log.info("Uploaded files saves successfully.")

        except Exception as e:
            self.log.error(f"Error saving PDF: {e}")
            raise DocumentPortalException("An error occurred while saving the PDF.", sys)

    def read_pdf(self, pdf_path: Path) -> str:
        """
        Reads a PDF file and extracts text from each page
        """
        try:
            with fitz.open(self, pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted and cannot be read: {pdf_path.name}.")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.srtip():
                        all_text.append(f"\n --- Page {page_num + 1} -- \n{text}")
                self.log.info("PDF red successfully", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("An error occurred while readin the PDF.", sys)
        
    def combine_documents(self) -> str:
        """
        Concatenate 
        """
        try:
            content_dict = {}
            doc_parts = {}

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined", count=len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combingin documents.", sys)