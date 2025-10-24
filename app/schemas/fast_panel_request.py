from pydantic import BaseModel
from typing import List, Optional

class FastSearchFilters(BaseModel):
    count: Optional[int]
    gender: Optional[str]
    filters: Optional[List[str]]

class FastNaturalSearch(BaseModel):
    question: str
    mode: str
    filters: Optional[FastSearchFilters]