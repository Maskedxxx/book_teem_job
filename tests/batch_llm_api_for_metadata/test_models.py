from pydantic import BaseModel
from typing import List, Optional

class Quote(BaseModel):
    id: int
    text: str
    author: str

class Metadata(BaseModel):
    isChapterStart: bool
    partTitle: Optional[str]
    quotes: List[Quote]
    summary: str
    keywords: List[str]

class BookPage(BaseModel):
    pageNumber: int
    content: str
    metadata: Metadata

class PageAnalysisResult(BaseModel):
    summary: str
    keywords: List[str]