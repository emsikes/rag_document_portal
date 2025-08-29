import io
import sys
from pathlib import Path
from src.document_compare.data_ingestion import DocoumentIngestion
from src.document_compare.document_compare import DocumentCompareLLM

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

# ---- Setup: Load local PDF files as if they were "uploaded" ---- #
def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())  # simulate .getbuffer()

# ---- Step 1: Save and combine PDFs ---- #
def test_compare_documents():
    try:
        ref_path = ("C:\\Users\\cloud\\Documents\\projects\\llm-ops\\code\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
        act_path = ("C:\\Users\\cloud\\Documents\\projects\\llm-ops\\code\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")

        # Wrap them like Streamlit UploadedFile-style
        class FakeUpload:
            def __init__(self, file_path: Path):
                self.name = file_path.name
                self._buffer = file_path.read_bytes()

            def getbuffer(self):
                return self._buffer

        # Instantiate
        comparator = DocoumentIngestion()
        ref_upload = FakeUpload(ref_path)
        act_upload = FakeUpload(act_path)

        # Save files and combine
        ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
        combined_text = comparator.combine_documents()
        comparator.clean_old_sessions(keep_latest=3)

        print("\n Combined Text Preview (First 1000 chars):\n")
        print(combined_text[:1000])

        # ---- Step 2: Run LLM comparison ---- #
        llm_comparator = DocumentCompareLLM()
        df = llm_comparator.compare_documents(combined_text)
        
        print("\n Comparison DataFrame:\n")
        print(df)
    except Exception as e:
        raise DocumentPortalException("An error occurred.", sys)

if __name__ == "__main__":
    test_compare_documents()