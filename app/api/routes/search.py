# app/api/routes/search.py
from fastapi import APIRouter
from app.schemas.fast_panel_request import FastNaturalSearch
from app.schemas.fast_panel_response import FastNaturalSearchResponse, ChartFastResult

router = APIRouter()

@router.post("/search/natural", response_model=FastNaturalSearchResponse)
async def natural_search(request: FastNaturalSearch):
    # 지금은 임의의 데이터 반환
    return FastNaturalSearchResponse(
        accuracy=0.95,
        panelList=["w4006926436054", "w268969641180673"],
        accuracyList=[0.92, 0.97],
        charts=[
            ChartFastResult(
                chartType="bar",
                title="연령대 분포",
                reason="샘플 차트",
                xaxis="age",
                yaxis="count",
                panelColumn="연령대"
            )
        ]
    )
