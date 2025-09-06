import io
import sys
from pathlib import Path
from src.document_compare.data_ingestion import DocumentIngestion
from src.document_compare.document_compare import DocumentCompareLLM
from exception.custom_exception import DocumentPortalException


def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())

def test_compare_documents():
    try:
        ref_path = ("C:\\Users\\cloud\\Documents\\projects\\llm-ops\\code\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
        act_path = ("C:\\Users\\cloud\\Documents\\projects\\llm-ops\\code\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")

        class FakeUpload:
            def __init__(self, file_path: Path):
                self.name = file_path.name
                self._buffer = file_path.read_bytes()

            def getbuffer(self):
                return self._buffer
            
        comparer = DocumentIngestion()
        ref_upload = FakeUpload(ref_path)
        act_upload = FakeUpload(act_path)

        ref_file, act_file = comparer.save_uploaded_files(ref_upload, act_upload)
        combined_text = comparer.combine_documents()

        print("\n Combined Text Preview (First 1000 chars):\n")
        print(combined_text[:1000])

        llm_comparer = DocumentCompareLLM()
        comparisin_df = llm_comparer.compare_documents(combined_text)

        print("\n=== Comparison Results ===")
        print(comparisin_df.head())
    except Exception as e:
        raise DocumentPortalException("An error occurred during document_compare.", sys)

    
test_compare_documents()