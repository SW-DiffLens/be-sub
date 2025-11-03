from pydantic import BaseModel
from typing import List, Optional

class FastSearchFilters(BaseModel):
    count: Optional[int] = None
    gender: Optional[str] = None
    filters: Optional[List[str]] = None

class FastNaturalSearch(BaseModel):
    question: str
    mode: str
    filters: Optional[FastSearchFilters] = None