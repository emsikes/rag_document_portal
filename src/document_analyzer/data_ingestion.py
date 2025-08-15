import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentHandler:
    """
    Save and read files (PDFs) and log all actions.  
    Supports session-based organization by creating a new directory for each session.
    """
    def __init__(self, data_dir=None, session_id=None):
        self.log=None
        try:    
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                "DATA_STORAGE_PATH",
                os.path.join(os.getcwd(), "data", "document_analyzer")
            )

            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

            # Create session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            print(f"DEBUG: Session directory created: {self.session_path}")
            print(f"DEBUG: Directory exists: {os.path.exists(self.session_path)}")

            self.log.info(f"DocumentHandler initialized", session_id=self.session_id, session_path=self.session_path)

        except Exception as e:
            if self.log:
                self.log.error(f"Error initializing DocumentHandler: {e}")
            else:
                print(f"Error initializing DocumentHandler (no logger: {e})")
            raise DocumentPortalException("Error initiating DocumentHandler", e) from e
        

    def save_pdf(self, uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Invalid file type.  Only PDFs are allowed.")
            
            save_path = os.path.join(self.session_path, filename)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            self.log.info("PDF saved successfully", file=filename, save_path=save_path, session_id=self.session_id)

            return save_path

        except Exception as e:
            self.log.error(f"Error saving PDF: {e}")
            raise DocumentPortalException("Error saving PDF", e) from e

    def read_pdf(self, pdf_path:str) -> str:
        try:
            text_chunks = []

            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text_chunks.append(f"\n--- Page {page_num} ---\n{page.get_text()}")
            text = "\n".join(text_chunks)

            self.log.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id)

            return text

        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("Error reading PDF", e) from e
        

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    # handler = DocumentHandler()

    # pdf_path = r"C:\\Users\\cloud\\Documents\\projects\\llm-ops\\code\\document_portal\\data\\document_analysis\\9781835087985-ADVERSARIAL_AI_ATTACKS_MITIGATIONS_AND_DEFENSE_STRATEGIES.pdf"

    # class TestFile:
    #     def __init__(self, file_path):
    #         self.name = Path(file_path).name
    #         self._file_path = file_path
    #     def getbuffer(self):
    #         with open(self._file_path, "rb") as f:
    #             return f.read()
        
    
    # try:
    #     print(f"DEBUG: Current working directory: {os.getcwd()}")
    #     print(f"DEBUG: PDF file exists: {os.path.exists(pdf_path)}")

    #     test_file = TestFile(pdf_path)
    #     handler = DocumentHandler(session_id="test_session")   

    #     saved_path = handler.save_pdf(test_file)
    #     print(f"SUCCESS: PDF saved to: {saved_path}") 

    #     content = handler.read_pdf(saved_path)
    #     print("PDF Content:")
    #     print(content[:500])

    # except Exception as e:
    #     print(f"Error: {e}")
    #     import traceback
    #     traceback.print_exc()


