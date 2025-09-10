import os
from pathlib import Path
from src.document_analyzer.data_ingestion import DocumentHandler
from src.document_analyzer.data_analysis import DocumentAnalyzer



PDF_PATH = r"C:\\Users\\cloud\\Documents\\projects\\llm-ops\\code\\document_portal\\data\\document_analysis\\9781803246284-DATA_ENGINEERING_WITH_DBT.pdf"

class TestFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path
    def getbuffer(self):
        return open(self._file_path, "rb").read()
    
def main():
    try:

        print(f"DEBUG: Current working directory: {os.getcwd()}")
        print(f"DEBUG: PDF file exists: {os.path.exists(PDF_PATH)}")

        # Test file ingestion
        test_file = TestFile(PDF_PATH)
        handler = DocumentHandler(session_id="test_session_test_py")   

        saved_path = handler.save_pdf(test_file)
        print(f"SUCCESS: PDF saved to: {saved_path}") 
        
        text_content = handler.read_pdf(saved_path)
        print(f"Extracted text length: {len(text_content)} chars\n")

        # Test document analysis
        analyzer = DocumentAnalyzer() # Load LLM and OutputParser
        anaysis_result = analyzer.analyze_document(text_content)
    
        # Display results
        print(f"\n=== Metadata Analysis Result ===")
        for key, value in anaysis_result.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()