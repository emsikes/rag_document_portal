import uuid
from pathlib import Path
import sys
from datetime import datetime, timezone

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader



class DocumentIngestor:
    SUPPORTED_FILE_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md'}
    def __init__(self, temp_dir: str = "/data/multi_doc_chat", faiss_dir: str = "faiss_index", session_id: str | None = None):
        try:
            self.log = CustomLogger().get_logger(__name__)

            # Base directories
            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)

            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            # Session directories
            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id

            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)

            # Load Models
            self.model_loader = ModelLoader()
            self.log.info(
                "DocumentIngestor initialized",
                temp_base=str(self.temp_dir),
                faiss_base=str(self.faiss_dir),
                temp_path=str(self.session_temp_dir),
                faiss_path=str(self.session_faiss_dir)
            )

        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor", error=str(e))
            raise DocumentPortalException("Error initializing DocumentIngestor", sys)

    def ingest_file(self, uploaded_file):
        try:
            documents = []

            # Validate supported file extentsion type
            for file in uploaded_file:
                ext = Path(uploaded_file.name).suffix.lower()
                if not ext in self.SUPPORTED_FILE_EXTENSIONS:
                    self.log.warning("Unsupported file type - file will be skipped", filename=uploaded_file.name)
                    continue
                unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
                temp_path = self.session_temp_dir / unique_filename

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                self.log.info("File successfully saved for ingestion", filename=uploaded_file.name, saved_as=str(temp_path), session_id=self.session_id)

                if ext == ".pdf":
                    loader = PyPDFLoader(str(temp_path))
                elif ext == ".docs":
                    loader = Docx2txtLoader(str(temp_path))
                elif ext == ".txt":
                    loader = UnstructuredMarkdownLoader(str(temp_path), encoding="utf8")
                elif ext == ".md":
                    loader = TextLoader(str(temp_path), encoding="utf8")
                else:
                    self.log.warning("Unsupported file type - file will be skipped", filename=uploaded_file.name)
                    continue

                docs = loader.load()
                documents.extend(docs)

            if not documents:
                raise DocumentPortalException("No valid documents loaded", sys)
            self.log.info("All documents loaded", total_docs=len(documents), session_id=self.session_id)

            return self.__create_retriever(documents)       

        except Exception as e:
            self.log.error("Failed to ingest file", error=str(e))
            raise DocumentPortalException("Error ingesting file in DocumentIngestor", sys)

    def __create_retriever(self, documents):
        try:
            embeddings = ModelLoader().load_embeddings()
            vectorstore = FAISS.from_documents(documents, embeddings)
            return vectorstore.as_retriever()
        except Exception as e:
            self.log.error("Failed to create retriever", error=str(e))
            raise DocumentPortalException("Error creating retriever in DocumentIngestor", sys)
