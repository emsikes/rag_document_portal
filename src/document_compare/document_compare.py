import sys
from dotenv import load_dotenv
import os
import pandas as pd

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from models.models import *
from prompts.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader

from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentCompareLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_prser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
        self.prompt = PROMPT_REGISTRY.get("document_compare")
        self.chain = self.prompt | self.llm | self.parser | self.fixing_prser
        self.log.info("DocumentCompareLLM initialized with model and parser")

    def compare_documents(self):
        """ 
        Compares two documents and returns a structured comparison
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in compare_documents: {e}")
            raise DocumentPortalException("An error occurred while comparing documents.", sys)

    def _format_response(self):
        """ 
        Formats the response from the LLM into a structured output format
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error formatting response in DataFrame: {e}")
            raise DocumentPortalException("An error occurred while formatting the response DataFrame.", sys)