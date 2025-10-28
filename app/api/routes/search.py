# app/api/routes/search.py
from fastapi import Depends, APIRouter
from app.schemas.fast_panel_request import FastNaturalSearch
from app.schemas.fast_panel_response import FastNaturalSearchResponse, ChartFastResult
from typing import List, Dict, Any

# db 정보
from app.config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = APIRouter()

@router.post("/search/natural", response_model=FastNaturalSearchResponse)
async def natural_search(request: FastNaturalSearch):
    # 지금은 임의의 데이터 반환
    return FastNaturalSearchResponse(
        accuracy=0.95,
        panelList=["w100010279508856", "w100012191331982", "w100016436830399", "w100033373262592", "w100037166280318", "w10005233127332", "w100059715520037"],
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

# DB 활용 예시
# Member 테이블의 데이터를 불러옵니다.
@router.get("/search/test", response_model=List[Dict[str, Any]])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM member"))
    return result.mappings().all()
