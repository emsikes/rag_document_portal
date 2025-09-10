# RAG Document Portal

![RAG Document Portal Banner](A_header_image_for_the_"RAG_Document_Portal"_featu.png)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/streamlit-app-red.svg)](https://streamlit.io/)  
[![LangChain](https://img.shields.io/badge/LangChain-framework-lightblue.svg)](https://www.langchain.com/)  
[![FAISS](https://img.shields.io/badge/FAISS-vector%20store-teal.svg)](https://github.com/facebookresearch/faiss)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](#-contributing)

A lightweight, easy-to-use **Retrieval-Augmented Generation (RAG)** powered portal for exploring, summarizing, and comparing documents through a simple web interface.  
Built for AI developers, data engineers, and researchers who want a practical sandbox to experiment with RAG workflows.

---

## ✨ Features

- 📂 **Document Uploads** – Add and manage documents directly from the portal.  
- 🔍 **Semantic Search** – Ask natural language questions across single or multiple documents.  
- 📝 **Summarization** – Generate concise summaries of uploaded content.  
- ⚖️ **Document Comparison** – Place two documents side by side for quick comparison.  
- 💬 **Conversational Interface** – Chat with your documents to uncover insights.  

---

## 🛠️ Tech Stack

- **Python** – Core backend logic  
- **Streamlit** – Interactive, lightweight web UI  
- **LangChain** – Orchestration framework for RAG  
- **FAISS** – Vector similarity search for retrieval  

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/emsikes/rag_document_portal.git
cd rag_document_portal
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run streamlit_ui.py
```

The portal will be available in your browser at [http://localhost:8501](http://localhost:8501).

---

## 📂 Project Structure

```plaintext
rag_document_portal/
├── app.py              # Core backend orchestration
├── streamlit_ui.py     # Web UI entry point
├── requirements.txt    # Project dependencies
├── data/               # Example documents
└── utils/              # Helper functions and utilities
```

---

## 🤝 Contributing

Contributions are welcome!  
You can:
- Extend retrieval models  
- Improve summarization pipelines  
- Enhance the UI for better workflows  

Fork the repo, create a branch, and submit a pull request.

---

## 🎯 Roadmap

- [ ] Add support for additional embedding models  
- [ ] Enable multi-format document parsing (PDF, DOCX, TXT, etc.)  
- [ ] Improve multi-document conversation context  
- [ ] Add authentication & user management  

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and share.

---

## 🙌 Acknowledgements

Inspired by the growing ecosystem of **RAG applications**,  
built to make document interaction more intuitive and powerful.
