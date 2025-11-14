import os
from typing import List, Optional, Any, Dict
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.document_ingestion.data_ingestion import (
    DocumentHandler, 
    DocumentCompare, 
    ChatIngestor, 
    FaissManager)
from src.document_analyzer.data_analysis import DocumentAnalyzer
from src.document_compare.document_compare import DocumentCompareLLM
from src.document_chat.retrieval import ConversationalRAG



app = FastAPI(title="Document Portal API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve static web content
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

def _read_pdf_via_handler(handler: DocumentHandler, path: str) -> str:
    """
    Helper function to read PDFs using the DocumentHandler
    """
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading PDF: {str(e)}")
    
class FastAPIFileAdapter:
    """
    Adapt FastAPI UploadFile -> .name + .getbuffer() API - gets the file in the buffer for later processing
    """
    def __init__(self, uf: UploadFile):
        self._uf = uf
        self.name = uf.filename

    def getbuffer(self) -> bytes:
        self.uf_file.seek(0)

        return self._uf.file.read()


@app.get("/", response_class=HTMLResponse)
async def server_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "document-portal"}


@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)) -> Any:
    try:
        document_handler = DocumentHandler()
        saved_path = document_handler.save_pdf(FastAPIFileAdapter(file))
        text = _read_pdf_via_handler(document_handler, saved_path)

        document_analyzer = DocumentAnalyzer()
        result = document_analyzer.analyze_document(text)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Analysis failed: {e}")
    
    
@app.post("/compare")
async def compare_documents(refernce: UploadFile = File(...), actual: UploadFile = File(...)) -> Any:
    try:
        doc_compare = DocumentCompare()
        ref_path, act_path = doc_compare.save_uploaded_files(FastAPIFileAdapter(refernce), FastAPIFileAdapter(actual))
        _ = ref_path, act_path
        combined_text = doc_compare.combine_documents()
        compare = DocumentCompareLLM()
        final_comparison = compare.compare_documents(combined_text)
        
        return {"rows": final_comparison.to_dict(orient="records"), "session_id": doc_compare.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Document comparison failed: {e}")

 
@app.post("/chat/index")
async def chat_build_index(
        files: List[UploadFile] = File(...),
        session_id: Optional[str] = Form(None),
        use_session_dirs: bool = Form(True),
        chunk_size: int = Form(1000),
        chunk_overlap: int = Form(200),
        k: int = Form(5),
    ) -> Any:
    try:
        wrapped = [FastAPIFileAdapter(f) for f in files]
        chat_ingestor = ChatIngestor(
            temp_base=UPLOAD_BASE,
            faiss_base=FAISS_BASE,
            use_session_dirs=use_session_dirs,
            session_id=session_id or None,
        )
        chat_ingestor.build_retriever(wrapped, chunk_size=chunk_size, chunk_overlap=chunk_overlap, k=k)

        return {"session_id": chat_ingestor.session_id, "k": k, "use_session_dirs": use_session_dirs}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Indexing failed: {e}")


@app.post("/chat/query")
async def chat_query(
    question: str = Form(...),
    session_id: Optional[str] = Form(None),
    use_session_dirs: bool = Form(True),
    k: int = Form(5)
) -> Any:
    try:
        if use_session_dirs and not session_id:
            raise HTTPException(status_code=400, detail="session_id is required when use_session_dirs=True")
        
        # Define FAISS index path
        index_dir = os.path.join(FAISS_BASE, session_id) if use_session_dirs else FAISS_BASE #type: ignore
        if not os.path.isdir(index_dir):
            raise HTTPException(status_code=404, detail=f"FAISS index not found at: {index_dir}")
        
        # Initialize LCEL RAG pipeline
        rag = ConversationalRAG(session_id=session_id) #type: ignore
        rag.load_retriever_from_faiss(index_dir)

        # Optional: Pass empty chat history
        response = rag.invoke(question, chat_history=[])

        return {
            "answer": response,
            "session_id": session_id,
            "k": k,
            "engine": "LCEL-RAG"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, details=f"Query failed: {e}")