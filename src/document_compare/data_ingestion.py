import sys
import uuid
from pathlib import Path
import fitz
from datetime import datetime, timezone

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentIngestion:
    """
    Handles saving, reading, and combing PDFs for comparisin with session-based versioning
    """
    def __init__(self, base_dir: str = "data/document_compare", session_id=None):
        self.log = CustomLogger.get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.log.info("Document Compare initiated", session_path=str(self.session_path))


    def save_uploaded_files(self, reference_file, actual_file):
            """
            Save reference and actual PDF files in the session directory
            """

            try:
                ref_path = self.session_path / reference_file.name
                act_path = self.session_path / actual_file.name

                if not reference_file.name.lower().endswith(".pdf") or not actual_file.name.lower().endswith(".pdf"):
                    raise ValueError("Only PDF files are allowed.")
                
                with open(ref_path, "wb") as f:
                    f.write(reference_file.getbuffer())

                with open(act_path, "wb") as f:
                    f.write(actual_file.getbuffer())

                self.log.info("Files saved", reference=str(ref_path), actual=str(act_path), session=self.session_id)
                
                return ref_path, act_path

            except Exception as e:
                self.log.error("Error saving PDF files", error=str(e), session=self.session_id)
                raise DocumentPortalException("An error occurred while saving the files.", sys)

    def read_pdf(self, pdf_path: Path) -> str:
        """
        Reads a PDF file and extracts text from each page
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted and cannot be read: {pdf_path.name}.")
                
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.srtip():
                        all_text.append(f"\n --- Page {page_num + 1} --- \n{text}")

                self.log.info("PDF read successfully", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)
            
        except Exception as e:
            self.log.error("Error reading PDF:", file=str(pdf_path), error=str(e))
            raise DocumentPortalException("An error occurred while reading the PDF.", sys)
        
    def combine_documents(self) -> str:
        """
        Combine content of all PDFs in session folder into a single string.
        """
        try:
            doc_parts = []
            for file in sorted(self.session_path.iterdir()):
                if file.is_file() and file.suffix.lower() == ".pdf":
                    content = self.read_pdf(file)
                    doc_parts.append(f"Document: {file.name}\n{content}")

            combined_text = "\n\n.join(doc_parts)"
            self.log.info("Documents combined", count=len(doc_parts), session=self.session_id)

            return combined_text
        
        except Exception as e:
            self.log.error("Error combining documents", error=str(e), session=self.session_id)
            raise DocumentPortalException("Error combining documents", sys)
        
    def clean_old_sessions(self, keep_latest=5):
        try:
            session_folders = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()],
                reverse=True
            )
            for folder in session_folders[keep_latest: ]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.log.info("Stale session folder deleted", path=str(folder))

        except Exception as e:
            self.log.error("Error cleaning stale sessions", error=str(e))
            raise DocumentPortalException("Error cleaning stale sessions", sys)