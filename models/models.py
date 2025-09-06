from pydantic import BaseModel, RootModel, Field
from typing import Optional, List, Dict, Any, Union
from enum import Enum


class MetaData(BaseModel):
    Summary: List[str] = Field(default_factory=list, description="Summary of the document")
    Title: str
    Author: str
    DataCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageContent: Union[int, str] # Optional, can be "not available"
    SentimentTone: str

class ChangeFormat(BaseModel):
    Page: str
    changes: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass

class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISIN = "document_comparisin"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"
