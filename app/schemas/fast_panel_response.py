from pydantic import BaseModel
from typing import List, Optional

class ChartFastResult(BaseModel):
    chartType: str
    title: str
    reason: str
    xaxis: str
    yaxis: str
    panelColumn: str

class FastNaturalSearchResponse(BaseModel):
    accuracy: Optional[float]
    panelList: List[str]
    accuracyList: List[float]
    charts: List[ChartFastResult]