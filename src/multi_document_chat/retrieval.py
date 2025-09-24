import sys
import os
from operator import itemgetter
from typing import Optional, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.messages import BaseMessage
from langchain_community.vectorstores import FAISS

from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from prompts.prompt_library import PROMPT_REGISTRY
from models.models import PromptType



class ConversationalRAG:
    def __init__(self, session_id: str, retriever=None):

        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.llm = self.__load_llm()
            self.contextualize_prompt: ChatMessagePromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.vaue]
            self.qa_prompt: ChatMessagePromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            if retriever is None:
                raise ValueError("Retriever cannot be None")
            self.retriever = retriever
            self._buid_lcel_chain()
            self.log.info("ConverationalRAG initialized", session_id=self.session_id)

        except Exception as e:
            self.log.error("Failed to initialize COnversationalRAG", error=str(e))
            raise DocumentPortalException("Initialization error in ConversationalRAG", sys)


    def load_retriever_from_faiss(self, index_path: str):
        """
        Load FAISS vectorstore from disk and convert to retriever
        """

        try:
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            
            vectorstore = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True, # only set this if the inde is trusted
            )

            self.retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            self.log.info("FAISS retriever loaded successfully", index_path=index_path, session_id=self.session_id)

            self._buid_lcel_chain()
            return self.retriever

        except Exception as e:
            self.log.error("Failed to load retriever from FAISS", error=str(e))
            raise DocumentPortalException("Error loading retriever in ConversationalRAG", sys)


    def invoke(self, user_input: str, chat_history: Optional[List[BaseMessage]] = None) -> str:

        try:
            chat_history = chat_history or []
            payload = {"input": user_input, "chat_history": chat_history}
            answer = self.chain.invoke(payload)
            if not answer:
                self.log.warning('No answer generatee', user_input=user_input, session_id=self.session_id)
                return "No answer generated."
            
            self.log.info("Chain invoked successfully,",
                 session_id=self.session_id,
                 user_input=user_input,
                 answer_preview=answer[:150],    
            )
            return answer

        except Exception as e:
            self.log.error("Failed to invoke ConversationalRAG", error=str(e))
            raise DocumentPortalException("Invokation error in ConversationalRAG", sys)

    def __load_llm(self):
        
        try:
            llm = ModelLoader().load_llm()
            if not llm:
                raise ValueError("LLM could not be loaded")
            self.log.info("LLM loaded successfully", session_id=self.session_id)

            return llm
        except Exception as e:
            self.log.error("Failed to load LLM", error=str(e))
            raise DocumentPortalException("Error loading LLM in ConversationalRAG", sys)

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    def _buid_lcel_chain(self):
        
        try:
            # Rewrite question using chat history
            question_rewriter = (
                {"input": itemgetter("input"), "chat_history": itemgetter("chat_history")}
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser
            )

            # Retrieve docs for rewritten question
            retrieve_docs = self.retriever | self._format_docs

            # Feed context + original input + chat history in answer prompt
            self.chain = (
                {
                    "context": retrieve_docs,
                    "input": itemgetter("input"),
                    "chat_history": itemgetter("chat_history"),
                }
                | self.qa_prompt
                | self.llm
                | StrOutputParser()
            )

            self.log.info("LCEL chain create successfully", session_id=self.session_id)

        except Exception as e:
            self.log.error("Faied to buid LCEL chain", error=str(e))
            raise DocumentPortalException("Error building LCEL chain in ConversationalRAG")